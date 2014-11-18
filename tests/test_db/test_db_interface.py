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

import nose.tools as nt
import importlib

from xpensemate.db.interface.factory import DatabaseInterfaceFactory
from xpensemate.db.proxy.postgres.deployment import reset_database
from xpensemate.config import DBConfig
import xpensemate.data_types as dt


class TestInsertQueryPsycopg2:
    
    @classmethod
    def setUpClass(cls):
        reset_database()
        cls.db_interface = DatabaseInterfaceFactory.get_interface()
    
    @classmethod
    def tearDownClass(cls):
        reset_database()
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def make_member(self, name, password):
        member = dt.MemberWithCredentials(name=name, password=password, active=True)
        return member
        
    @nt.raises(Exception)
    def test_missing_member(self):
        member = self.db_interface.get_member_credentials("Missing member")
        
    @nt.raises(Exception)
    def test_insert_duplicate_member(self):
        member = self.make_member("Duplicate member", "pass")
        self.db_interface.insert_member(member)
        self.db_interface.insert_member(member)
    
    def test_insert_member(self):
        member = self.make_member("New member", "pass")
        self.db_interface.insert_member(member)
        member2 = self.db_interface.get_member_credentials(member.name)
        nt.assert_equal(member.__class__, member2.__class__, "Bad type returned")
        nt.assert_equal(member2.__dict__, member.__dict__, "Wrong member details returned")
    
    @nt.nottest
    def test_get_groups_no_group(self):
        pass
        
    @nt.nottest
    def test_get_groups_2_groups(self):
        pass

