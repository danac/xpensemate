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
from xpensemate.data_types import Group
from xpensemate.web import forms
from xpensemate.web import validation

# Get an instance of the backend interface
db_interface = DatabaseInterfaceFactory.get_interface()

#: Flask application blueprint implementing the group/<group_id> route
blueprint = flask.Blueprint('groups', __name__)


def _insert_group():
    member_name = flask.session['username']
    group_name = flask.request.form['group_name']
    smallest_unit = flask.request.form['smallest_unit']
    
    new_group = Group(group_name,
                      smallest_unit,
                      member_name,
                      {member_name:0.0})
                      
    db_interface.insert_group(new_group)
    flask.flash("Created group {}.".format(group_name), 'info')


def _delete_group():
    pass
    #group_id = flask.request.form['group_id']
    #db_interface.delete_group(group_id)
    #flask.flash("Deleted group " + str(group_id), 'info')

def _add_group_member():
    print("ADD MEMBER!", flask.request.form['member_name'], flask.request.form['group_id'])
    #group_id = flask.request.form['group_id']
    #db_interface.delete_group(group_id)
    #flask.flash("Deleted group " + str(group_id), 'info')

    
@blueprint.route("/groups", methods=['GET', 'POST'])
@blueprint.route("/groups/", methods=['GET', 'POST'])
def groups():
    """
    Page displaying the user's groups.
    
    Served on the following routes:
    * /groups
    * /groups/
    """
    
    if 'username' not in flask.session:
        return flask.redirect('/login')
        
    member_name = flask.session['username']
    groups = db_interface.get_member_groups(member_name)
    
    group_form = forms.GroupForm(flask.request.form)
    new_member_form = forms.NewMemberForm(flask.request.form)

    if flask.request.method == 'POST':
        redirect = False
        if flask.request.form['action'] == 'new_member':
            if new_member_form.validate():
                redirect = True
                validation.db_access_wrapper(_add_group_member)
            else:
                validation.flash_form_errors(new_member_form)
        else:
            redirect = validation.process_new_delete_form(group_form, _insert_group, _delete_group)
            
        if redirect:
            return flask.redirect('/groups')
        
    return flask.render_template("groups.htm", groups=groups, member_name=member_name, group_form=group_form, new_member_form=new_member_form)
