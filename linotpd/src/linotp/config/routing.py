# -*- coding: utf-8 -*-
#
#    LinOTP - the open source solution for two factor authentication
#    Copyright (C) 2010 - 2014 LSE Leading Security Experts GmbH
#
#    This file is part of LinOTP server.
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public
#    License, version 3, as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the
#               GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    E-mail: linotp@lsexperts.de
#    Contact: www.linotp.org
#    Support: www.lsexperts.de
#

"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""

from pylons import config
from routes import Mapper

def make_map(global_conf, app_conf,):
    '''
    Create, configure and return the routes Mapper
    There are the three main controllers:
        /admin
        /validate
        /system
    '''
    routeMap = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    routeMap.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved

    routeMap.connect('/error/{action}', controller='error')
    routeMap.connect('/error/{action}/{id}', controller='error')

    routeMap.connect('/{controller}/{action}')
    routeMap.connect('/{controller}/{action}/{id}')

    # the first / - default will be taken!!

    # in case of selfservice, we route the default / to selfservice
    selfservice = app_conf.get('service.selfservice', 'True') == 'True'
    if selfservice:
        routeMap.connect('/selfservice/custom-style.css', controller='selfservice', action='custom_style')
        routeMap.connect('/selfservice', controller='selfservice', action='index')
        routeMap.connect('/', controller='selfservice', action='index')

    # in case of manage, we route the default / to manage
    manage = app_conf.get('service.manage', 'True') == 'True'
    if manage:
        routeMap.connect('/manage/custom-style.css', controller='manage', action='custom_style')
        routeMap.connect('/admin', controller='admin', action='show')
        routeMap.connect('/system', controller='system', action='getConfig')
        routeMap.connect('/manage/', controller='manage', action='index')
        routeMap.connect('/', controller='manage', action='index')

    # in case of validate, we route the default / to validate
    validate = app_conf.get('service.validate', 'True') == 'True'
    if validate:
        routeMap.connect('/validate', controller='validate', action='check')
        routeMap.connect('/', controller='validate', action='check')


    openid = app_conf.get('service.openid', 'True') == 'True'
    if openid:
        # the default openid will be the status
        routeMap.connect('/openid/', controller='openid', action='status')

    return routeMap
