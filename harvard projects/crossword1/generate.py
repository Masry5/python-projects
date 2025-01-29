from copy import deepcopy
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        '''
        print(self.domains)
        self.enforce_node_consistency()
        
        print('--------------------------------------------------------------------')
        print(self.domains)
        print('--------------------------------------------------------------------')
        self.revise(Variable(0, 1, 'down', 5),Variable(0, 1, 'across', 3))
        print(self.domains)
        print(self.crossword.overlaps[Variable(0, 1, 'down', 5),Variable(0, 1, 'across', 3)])
        print('--------------------------------------------------------------------')
        self.ac3()
        print(self.domains)
        ass={ Variable(0, 1, 'down', 5): 'SEVEN',Variable(0, 1, 'across', 3): {'SIX'},Variable(4, 1, 'across', 4): {'NINE'}}
        print(self.select_unassigned_variable(ass))'''
        
    
        
    
    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        Variables_copy=deepcopy(self.domains)
        for v in Variables_copy:
            for word in Variables_copy[v]:
                if len(word) != v.length:
                    self.domains[v].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision=False
        if self.crossword.overlaps[x,y] == None:
            return revision
        else:
            over=self.crossword.overlaps[x,y]
            i=over[0]
            j=over[1]
            
            x_copy=deepcopy(self.domains[x])
            for word1 in x_copy:
                nomodify=False
                for word2 in self.domains[y]:
                    if word1[i]== word2[j]:
                        nomodify= True
                        break
                if nomodify==False:
                    self.domains[x].remove(word1)
                    revision=True
            return revision
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs== None:
            queue=[]
        else:
            queue=arcs
        for var1 in self.domains:
            for var2 in self.domains:
                if var1==var2:
                    continue
                queue.append((var1,var2))
        while queue !=[]:
            (x,y)=queue.pop(0)
            if self.revise(x,y):
                if len(self.domains[x]) ==0:
                    return False
                for z in Crossword.neighbors(self.crossword,x):
                    if z == y:
                        continue
                    queue.append((z,x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment or len(assignment[var])<1:
                return False
        return True
 

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        ''' all values are distinct  '''
        for x in assignment:
            for y in assignment:
                if x==y:
                    continue
                if assignment[x]==assignment[y]:
                    return False
        '''  every value is the correct length'''
        for var in assignment:
            if len(assignment[var])!= var.length:
                return False
        '''  there are no conflicts between neighboring variables'''
        neighbors=Crossword.neighbors(self.crossword,var)
        done=[]
        for x in assignment:
            done.append(x)
            if len(assignment[x])==0:
                continue
            for y in assignment:
                if y in done or len(assignment[y])==0:
                    continue
                elif self.crossword.overlaps[x,y] ==None:
                    continue
                else:
                    (i,j)=self.crossword.overlaps[x,y]
                    xword=assignment[x]
                    yword=assignment[y]
                    if xword[i]!=yword[j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        if len(assignment)<3:
            return list(self.domains[var])
        
        values={g:0 for g in self.domains[var]}
        neighbors=Crossword.neighbors(self.crossword,var)
        for word1 in self.domains[var]:
            for neighbor in neighbors:
                if neighbor not in assignment:
                    for word2 in self.domains[neighbor]:
                        (i,j)=self.crossword.overlaps[var,neighbor]
                        if  word1[i]==word2[j]:
                            values[word1]+=1
        sorted_values =dict(sorted(values.items(), key=lambda x: x[1]) ,reversed=True)                                    
        return list(sorted_values.keys())

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        '''for var in self.domains:
            if var not in assignment:
                return var
        '''
        values={}
        counter=0
        for var in self.domains:
            if var in assignment:
                continue
            else:
                values[var]=len(self.domains[var])
                counter+=1
        if counter==1:
            values=list(values)
            return values[0]
        sorted_values =sorted(values.items(), key=lambda x: x[1])
        #return based on values
        if sorted_values[0][1]<sorted_values[1][1]:
            return sorted_values[0][0]
        else:    
            #get equal items
            degreedic={}
            smallestvalue=sorted_values[0][1]
            degreedic[sorted_values[0][0]]=smallestvalue
            sorted_values =dict( sorted(values.items(), key=lambda x: x[1]))
            for var in sorted_values:
                if smallestvalue<sorted_values[var]:
                    break
                elif smallestvalue==sorted_values[var]:
                    degreedic[var]=smallestvalue
            for var in degreedic:
                degreedic[var]=len(Crossword.neighbors(self.crossword,var))
            sorted_degrees =sorted(degreedic.items(), key=lambda x: x[1],reverse=True)
            
            return sorted_degrees[0][0] 
            
            
  

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        # Try a new variable
        var = self.select_unassigned_variable(assignment)
        domain=self.order_domain_values(var,assignment)
        for value in domain:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None
        


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
       creator.print(assignment)
       if output:
            creator.save(assignment, output)
   

if __name__ == "__main__":
    main()
