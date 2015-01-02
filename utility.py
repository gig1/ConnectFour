class Utility(object):
    def compute_utility(self, node, utilityplayer):
        pass


class SimpleUtility(Utility):
    def __init__(self, three_score, two_score):
        self.three_score = three_score
        self.two_score = two_score

    def compute_utility(self, node, utilityplayer):
        """
        Computes the utility of the node, using the following rules.

        * If utilityplayer has won, the score is 1,000,000
        * If utilityplayer has lost, the score is -1,000,000
        * Award self.three_score points for each three in a row and self.two_score
          points for each two in a row for utilityplayer.
        * Award -self.three_score points for each three in a row and -self.two_score points
          for each two in a row for the other player.
        * Finally, award one point if node.nodeplayer equals utilityplayer (it is currently
          utilityplayer's move), otherwise award -1 points.

        This function should only be called on a leaf.
        """

        # The match_in_direction function is very helpful here.  You will need to
        # loop through positions, adding up the score for various three or two in a
        # rows for each player.

        score = 0
        for row in range(6):
            for column in range(7):
                for (step_row, step_col) in [ (1,0), (0,1), (1,1), (1,-1) ]:
                    v = node.match_in_direction(row, column, step_row, step_col)
                    me = node.get_position(row, column) == utilityplayer
                    if v >= 4 and me:
                        return 1000000
                    elif v >= 4:
                        return -1000000
                    elif v == 3 and me:
                        score += self.three_score
                    elif v == 3:
                        score -= self.three_score
                    elif v == 2 and me:
                        score += self.two_score
                    elif v == 2:
                        score -= self.two_score

        if utilityplayer == node.nodeplayer:
            score += 1
        else:
            score -= 1

        return score


class WithColumnUtility(SimpleUtility):
    def __init__(self, three_score, two_score, column_scores):
        self.three_score = three_score
        self.two_score = two_score
        self.column_scores = column_scores

    def compute_utility(self, node, utilityplayer):
        score = super(WithColumnUtility, self).compute_utility(node, utilityplayer)

        col_scores = [1, 2, 3, 4, 3, 2, 1]
        for row in range(6):
            for col in range(5):
                v = node.get_position(row, col)
                if v != None and v == utilityplayer:
                    score += col_scores[col]
                elif v != None:
                    score -= col_scores[col]

        return score
