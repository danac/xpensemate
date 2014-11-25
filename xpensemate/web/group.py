#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014 Dana Christen
#
# This file is part of XpenseMate, a tool for managing shared expenses and
# hosted at https://github.com/danac/xpensemate.
#
# XpenseMate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import flask

from xpensemate.db.interface.factory import DatabaseInterfaceFactory
from xpensemate.web import validation
from xpensemate.web import forms
from xpensemate.data_types import Expense, Transfer
from xpensemate import exceptions


# Get an instance of the backend interface
db_interface = DatabaseInterfaceFactory.get_interface()

#: Flask application blueprint implementing the group/<group_id> route
blueprint = flask.Blueprint('group', __name__)


def _insert_expense(group):
    new_expense_members = []
    member_name = flask.session['username']
    group_id = group.group_id
    for member in group.member_balance:
        if member in flask.request.form:
            new_expense_members.append(member)
            
    new_expense = Expense(date=flask.request.form['date'],
                          description=flask.request.form['description'],
                          amount=flask.request.form['amount'],
                          maker=member_name,
                          members=new_expense_members)            
    
    allowed = member_name in group.members
    
    if allowed:
        db_interface.insert_expense(new_expense, group_id)
        flask.flash("New expense added.", "info")
    else:
        flask.flash("Authorization error.", "error")
        
    
def _insert_transfer(group):
    member_name = flask.session['username']
    group_id = group.group_id
            
    new_transfer = Transfer(date=flask.request.form['date'],
                            amount=flask.request.form['amount'],
                            from_member=member_name,
                            to_member=flask.request.form['to_member'])
    
    allowed = member_name in group.members
    
    if allowed:
        db_interface.insert_transfer(new_transfer, group_id)
        flask.flash("New transfer added.", "info")
    else:
        flask.flash("Authorization error.", "error")
    
    
def _delete_expense(group):
    expense_id = int(flask.request.form['expense_id'])
    group_expense_ids = [expense.expense_id for expense in group.expenses]
    allowed = expense_id in group_expense_ids
    if allowed:
        db_interface.delete_expense(expense_id)
        flask.flash("Expense deleted.", "info")
    else:
        flask.flash("Authorization error.", "error")
    
    
def _delete_transfer(group):
    transfer_id = int(flask.request.form['transfer_id'])
    group_transfer_ids = [transfer.transfer_id for transfer in group.transfers]
    allowed = transfer_id in group_transfer_ids
    db_interface.delete_transfer(flask.request.form['transfer_id'])
    if allowed:
        db_interface.delete_transfer(transfer_id)
        flask.flash("Transfer deleted.", "info")
    else:
        flask.flash("Authorization error.", "error")
    
    
@blueprint.route("/groups/<group_id>", methods=['GET', 'POST'])
def group(group_id):
    """
    Page displaying a detailed view of a group.
    :param int group_id: The ID of the group
    
    Served on the following routes:
        * /groups/<group_id>
    """
    
    if 'username' not in flask.session:
        return flask.redirect('/login')
        
    member_name = flask.session['username']

    group = db_interface.get_group_with_movements(group_id)
    groups = db_interface.get_member_groups(member_name)
    
    other_members = [p for p in group.members if p != member_name]
    ExpenseForm = forms.expense_form_factory(other_members)
    expense_form = ExpenseForm(flask.request.form)
    
    TransferForm = forms.transfer_form_factory(other_members)
    transfer_form = TransferForm(flask.request.form)
    
    if flask.request.method == 'POST':
        
        success = False
        
        if flask.request.form['form_name'] == "expense":
    
            success = validation.process_new_delete_form(expense_form, _insert_expense, _delete_expense, group, group)
            
        elif flask.request.form['form_name'] == "transfer":
            
            success = validation.process_new_delete_form(transfer_form, _insert_transfer, _delete_transfer, group, group)
        
        if success:
            return flask.redirect('/groups/' + group_id)
        
    return flask.render_template("group_expense.htm",
                                 group=group,
                                 groups=groups,
                                 expense_form=expense_form, 
                                 transfer_form=transfer_form, 
                                 member_name=member_name)
