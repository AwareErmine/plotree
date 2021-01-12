from copy import deepcopy

class plotree:
    """Make a story tree based on a list of lines

    Parameters:
    ==========
        text : list
            the list of lines
        opt_prefix : str
            the prefix used to indicate opt lines (default: "#")

    Attributes:
    ==========
        text : list
            the list of lines
        opt_prefix : str
            the prefix used to indicate opt lines (default: "#")
        jsonable : dict
            the tree made for the text

    Raises:
    ======
        plotProb
            Problem with the story's indentation
    """

    def __init__(self, text, opt_prefix="#", _last_line=None):
        self.text = text # Text list
        self.opt_prefix = opt_prefix # The prefix used for opts
        self._last_line = _last_line # The last line used in a branch
        self.jsonable = self._make_plotree() # Sets the tree as a param

    def clean_plotree(self, tree=None):
        if tree is None:
            tree = deepcopy(self.jsonable) # Otherwise we'd end up editing the tree directly!

        tree['plot'] = self._clean_line(tree['plot'])

        opts = tree['opts']
        if not opts:
            return tree # The end of a branch

        for idx, opt in enumerate(opts):
            opt['opt'] = self._clean_line(opt['opt'])
            self.clean_plotree(tree=opts[idx]['opt_to'])
        return tree

    def _clean_line(self, line):
        return line.replace(self.opt_prefix, "", 1).strip()

    def _make_plotree(self, line=None, tree=None):
        # Makes a tree based on the indenting of a txt file

        if line is None:
            line = self.text[0] # We start with the first line

        # Initiating the tree as either a plot or opt part
        if tree is None:
            if self._is_opt_line(line):
                raise plotProb(
                    f"Inconsistent indentation for line {self.text.index(new_opt_desc)}"
                    +"\nDon't start a story with options"
                )
            else:
                # Taking the next line
                try:
                    next_line = self.text[self.text.index(line)+1]
                except IndexError:
                    return self._plot_part(tree) # No next parts without a next line
                tree = self._plot_part(
                    line,
                    opts = [
                        self._make_branch(next_line)
                        ]
                    )

        # Finding the next line we're branching from or ending the looping
        try:
            new_opt_desc = self.text[self.text.index(self._last_line)+1]
        except IndexError:
            return tree # It's the end of the file if there isn't a next branch start

        # Finding the plot that action ties to
        branch_start = self._find_branch(new_opt_desc) # The root of the action
        if branch_start is None:
            raise plotProb(
                f"Inconsistent indentation for line {self.text.index(new_opt_desc)}"
            )

        # Editing the branch tied to the last line used
        edited_tree = self._edit_branch(
            tree=tree,
            root_plot=branch_start,
            new_opt_desc=new_opt_desc,
        )

        # We keep looping through the branches
        return self._make_plotree(
            line=self._last_line,
            tree=edited_tree,
        )

    def _make_branch(self, line):
        # Makes a branch from a line

        try:
            next_line = self.text[self.text.index(line)+1]
        except IndexError:
            self._last_line = line
            return self._plot_part(line) # It's the end if there is no next line

        part = self._give_part(line)

        # Making sure the next line is in the same branch
        if not self._same_branch(line, next_line):
            self._last_line = line
            return part

        # Make the associated branching
        if self._is_opt_part(part):
            part['opt_to'] = self._make_branch(next_line)
        else:
            part['opts'].append(self._make_branch(next_line))

        return part

    def _edit_branch(self, tree, root_plot, new_opt_desc):
        # Adds a new branching to a branch

        if self._is_opt_part(tree): # Only add branches as opts
            if root_plot in tree['opt']: # No options for options
                raise plotProb(
                    f"Inconsistent indentation for line {self.text.index(new_opt_desc)}"
                )
            self._plot_part = tree['opt_to']
        else:
            if root_plot in tree['plot']:
                tree['opts'].append(
                    self._make_branch(new_opt_desc)
                )
                return tree
            plot_part = tree

        for opt in plot_part['opts']:
            self._edit_branch(
                tree=opt['opt_to'],
                root_plot=root_plot,
                new_opt_desc=new_opt_desc,
            )
        return tree

    def _plot_part(self, line, opts=None):
        # Makes a plot part

        if opts is None:
            opts = []

        return {
            "plot" : line,
            "opts" : opts, # A list of opt_parts
        }

    def _opt_part(self, line, choice=None):
        # Makes an option part

        return {
            "opt" : line,
            "opt_to" : choice, # A plot_part
        }

    def _is_opt_line(self, line):
        # Checks if a line is an option or not

        return (
            line.strip().startswith(self.opt_prefix)
            )

    def _is_opt_part(self, part):
        # Checks if a part is an option or not

        return (
            "opt" in part
        )

    def _give_part(self, line):
        # Makes a plot/opt part based on a line

        if self._is_opt_line(line):
            return self._opt_part(line)
        else:
            return self._plot_part(line)

    def _find_branch(self, line):
        # Looks through the lines above a line for the parent branch

        loopable = self.text[self.text.index(line)::-1]
        for prior_line in loopable:
            if self._same_branch(prior_line, line):
                return prior_line
        return None

    def _same_branch(self, line, following_line):
        # Checks if the next line is part of the branch we're descending

        return (
            self._leading_spaces(line) < self._leading_spaces(following_line)
            )

    def _leading_spaces(self, line):
        # Returns the amount of indentation for a line

        return len(line)-len(line.strip(' '))

class plotProb(Exception): # Not a very fancy exception; I just wanted the name
    pass
