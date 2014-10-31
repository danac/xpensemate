***********************
Introduction and theory
***********************

This page introduces the context in which the XpenseMate project was born, and gives
an overview of features implemented in the program.


Where the idea comes from
=========================

Sharing expenses is very common among housemates or members of an association.
In a typical scenario, some members make a number of expenses on behalf of the group,
and every now and then, everyone gathers and those who paid less than their share
pay back those who spent more than their share. In the end, everyone has spent
the same overall amount of money.

When all expenses are fairly shared among the members, doing the maths is pretty
straightforward (even though it can be a bit tricky depending on the number of expenses
and team members).

Sharing expenses and settling debts
+++++++++++++++++++++++++++++++++++

However, when not all expenses involve the same members, settling the debts
can become a real challenge. Imagine a bunch of student friends living together
and sharing the household's bills. Assume that some of them visit their
families during the week-end while the others stay home. Even though they share
expenses such as the rent or the Internet connection fee, they decide that
the groceries bought for the weekend shouldn't be shared by those who aren't there.
Furthermore, imagine that some of them like to have lunch at home together while the others
stay at their workplaces. Knowing who owns how much to whom after a few weeks becomes
very tricky!

*XpenseMate* aims at solving this problem by providing an easy way to log expenses
and keep track of the debts among group members.


Simplifying debts
=================

In the scenario described in the previous section, not only is it hard to keep
track of the expenses, but it's also far from trivial to determine the optimal
way to settle the debts among people.

To illustrate this problem, let's look at an example.
Consider a group of 5 friends who share expenses,
where the number of people sharing an expense is not always the same, as
in the following table:

+------------+------+-----+---------+------+-----------+
| Amount     | People sharing the expense              |
+            +------+--------+------+------+-----------+
|            | Dana | Alizée | Mick | Loïc | Sébastien |
+============+======+========+======+======+===========+
| $ 3        | Yes  | Yes    | No   | No   | No        |
+------------+------+--------+------+------+-----------+
| $ 1.5      | Yes  | Yes    | Yes  | Yes  | Yes       |
+------------+------+--------+------+------+-----------+
| $ 2        | No   | No     | Yes  | No   | Yes       |
+------------+------+--------+------+------+-----------+
| ...        |      |        |      |      |           |
+------------+------+--------+------+------+-----------+

Imagine that at some point, the debts are calculated. What often happens is that everyone
ends up with a dept to someone else. Of course, in such a case it is easy to simplify the
situation by cancelling mutual debts -- in other words, if A owes $ 10 to B and B owes $ 5 to A,
A will simply give B $ 5.

While such simplifications reduce the number of debts, there can be still a large number of them.
Suppose that the debts of the group are given by the following table, where each row shows the debts
of a person, after trivial simplifications have been made (for example, the first row shows that
Dana owes $ 1 to Alizée, $ 2 to Mick and $ 1 to Loïc):

+------------+------------+------------+------------+------------+------------+------------+
|            |   Dana     |   Alizée   |   Mick     |   Loïc     | Sébastien  |            |
+------------+------------+------------+------------+------------+------------+------------+
|   Dana     |            |   $ 1      |   $ 2      |   $ 1      |  $ 0       | **$ 4**    |
+------------+------------+------------+------------+------------+------------+------------+
|   Alizée   |   $ 0      |            |   $ 0      |   $ 0      |  $ 0       | **$ 0**    |
+------------+------------+------------+------------+------------+------------+------------+
|   Mick     |   $ 0      |            |   $ 0      |   $ 0      |  $ 0       | **$ 0**    |
+------------+------------+------------+------------+------------+------------+------------+
|   Loïc     |   $ 0      |   $ 1.5    |   $ 5      |            |  $ 0       | **$ 6.5**  |
+------------+------------+------------+------------+------------+------------+------------+
|  Sébastien |   $ 0      |            |   $ 0      |   $ 1      |  $ 0       | **$ 1**    |
+------------+------------+------------+------------+------------+------------+------------+
|            | **$ 0**    | **$ 2.5**  | **$ 7**    | **$ 2**    | **$ 0**    |            |
+------------+------------+------------+------------+------------+------------+------------+

To better visualize the contents of this table, one can draw the following graph, where members are
assigned letters from A to E:

.. .. plot:: intro/plots/debt_graph.py
.. image:: /static/debt_graph_full.png


After giving a closer look at the previous graph, it can quickly be seen that
there are simpler ways to settle the debts.

The following graph shows the optimal solution:

.. image:: /static/debt_graph_simple.png

In summary, **when expenses are shared among members of a group and not all expenses
are shared by the same number of people, calculating the debts leads to an
excessively high number of money transfers**.


Partitioning and bipartite matching
===================================

*Coming soon...*


References
==========

* :download:`Tom Verhoeff, Settling Multiple Debts Efficiently: An Invitation to Computing Science </static/settling-debts.pdf>`
* `Subset Sum Problem on Wikipedia <http://en.wikipedia.org/wiki/Subset_sum_problem>`_
* `3-Partition Problem on Wikipedia <http://en.wikipedia.org/wiki/3-partition_problem>`_
