# Creado por Jorge Luis el 15/5/2013 12:31AM.
# Copyright (c) 2013. Jorge Luis, jota81, jcasado81 All rights reserved.

import sys

from genshi.builder import tag
from genshi.core import TEXT
from genshi.filters.transform import Transformer
from genshi.output import DocType

from trac.config import Option
from trac.core import *
from trac.config import ListOption
from trac.mimeview.api import get_mimetype
from trac.resource import Resource
from trac.ticket.api import TicketSystem
from trac.ticket.model import Ticket
from trac.ticket.notification import TicketNotifyEmail
from trac.ticket.web_ui import TicketModule
from trac.util.compat import set
from trac.util.translation import _
from trac.versioncontrol.web_ui.browser import BrowserModule
from trac.web.api import IRequestFilter, IRequestHandler, ITemplateStreamFilter
from trac.web.chrome import (add_script, add_stylesheet, INavigationContributor,
                             ITemplateProvider, prevnext_nav, Chrome, add_ctxtnav, add_meta)
from trac.wiki.admin import WikiAdmin

from trac.admin.web_ui import INavigationContributor

from themeengine.api import ThemeBase, ThemeEngineSystem
from trac.web.chrome import add_stylesheet, add_script

from pkg_resources import get_distribution, resource_filename
from urlparse import urlparse
from wsgiref.util import setup_testing_defaults

class ZurbTheme(ThemeBase):
    """Trac Zurb Theme."""

    template = htdocs = css = screenshot = disable_trac_css = True
    disable_all_trac_css = True

    ZURB_KEEP_CSS = set(
        (
            'diff.css',
            )
    )

    ZURB_TEMPLATE_MAP = {
        # Admin
        'admin_basics.html' : ('zurb_admin_basics.html', None),
        'admin_components.html' : ('zurb_admin_components.html', None),
        'admin_enums.html' : ('zurb_admin_enums.html', None),
        'admin_logging.html' : ('zurb_admin_logging.html', None),
        'admin_milestones.html' : ('zurb_admin_milestones.html', None),
        'admin_perms.html' : ('zurb_admin_perms.html', None),
        'admin_plugins.html' : ('zurb_admin_plugins.html', None),
        'admin_repositories.html' : ('zurb_admin_repositories.html', None),
        'admin_versions.html' : ('zurb_admin_versions.html', None),

        # Preferences
        'prefs_advanced.html' : ('zurb_prefs_advanced.html', None),
        'prefs_datetime.html' : ('zurb_prefs_datetime.html', None),
        'prefs_general.html' : ('zurb_prefs_general.html', None),
        'prefs_keybindings.html' : ('zurb_prefs_keybindings.html', None),
        'prefs_pygments.html' : ('zurb_prefs_pygments.html', None),
        'prefs_userinterface.html' : ('zurb_prefs_userinterface.html', None),

        # Search
        'search.html' : ('zurb_search.html', None),

        # Wiki
        'wiki_delete.html' : ('zurb_wiki_delete.html', None),
        'wiki_diff.html' : ('zurb_wiki_diff.html', None),
        'wiki_edit.html' : ('zurb_wiki_edit.html', None),
        'wiki_rename.html' : ('zurb_wiki_rename.html', None),
        'wiki_view.html' : ('zurb_wiki_view.html', None),

        # Ticket
        'milestone_edit.html' : ('zurb_milestone_edit.html', None),
        'milestone_delete.html' : ('zurb_milestone_delete.html', None),
        'milestone_view.html' : ('zurb_milestone_view.html', None),
        'query.html' : ('zurb_query.html', None),
        'report_delete.html' : ('zurb_report_delete.html', None),
        'report_edit.html' : ('zurb_report_edit.html', None),
        'report_list.html' : ('zurb_report_list.html', None),
        'report_view.html' : ('zurb_report_view.html', None),
        'ticket.html' : ('zurb_ticket.html', None),
        'ticket_change.html' : ('zurb_ticket_change.html', None),
        'ticket_box.html' : ('zurb_ticket_box.html', None),
        'ticket_preview.html' : ('zurb_ticket_preview.html', None),
        'ticket_delete.html' : ('zurb_ticket_delete.html', None),
        'batch_modify.html': ('zurb_batch_modify.html', None),

        # Attachment
        'attachment.html' : ('zurb_attachment.html', None),
        'preview_file.html' : ('zurb_preview_file.html', None),

        # Version control
        'revisionlog.html' : ('zurb_revisionlog.html', None),
        'diff_form.html' : ('zurb_diff_form.html', None),
        'browser.html' : ('zurb_browser.html', None),
        'changeset.html' : ('zurb_changeset.html', None),

        # General purpose
        'about.html' : ('zurb_about.html', None),
        'history_view.html' : ('zurb_history_view.html', None),
        'timeline.html' : ('zurb_timeline.html', None),
        'roadmap.html': ('zurb_roadmap.html', None),

        #Differences
        'diff_view.html' : ('zurb_diff_view.html', None),
        'diff_options.html' : ('zurb_diff_options.html', None),

        # Account manager plugin
        'login.html' : ('zurb_login.html', None),
        'prefs_um_profile.html' : ('zurb_prefs_um_profile.html', None),
        'reset_password.html' : ('zurb_reset_password.html', None),
        'register.html' : ('zurb_register.html', None),
        'prefs_account.html' : ('zurb_prefs_account.html', None),

        }

    Chrome.default_html_doctype = DocType.HTML5

    # INavigationContributor methods

    implements(INavigationContributor)

    def get_active_navigation_item(self, req):
        return

    def get_navigation_items(self, req):
        # The 'Admin' navigation item is only visible if at least one
        # admin panel is available
        if "TRAC_ADMIN" in req.perm:
            yield 'metanav', 'zadmin', tag.a(_('Admin'), href=req.href.admin(), title=_('Administration'))

    implements(IRequestFilter, ITemplateProvider)

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        """Nothing to do.
        """
        return handler

    def post_process_request(self, req, template, data, content_type):
        """Post process request filter.
        Removes all trac provided css if required"""
        #if "TRAC_ADMIN" in req.perm:
        #    add_ctxtnav(req, "Admin", "#", "Admin")

        add_meta(req, "width=device-width", http_equiv=None, name="viewport", scheme=None, lang=None)

        if self.is_active_theme:
            add_stylesheet(req, 'theme/css/foundation.css')
            add_stylesheet(req, 'theme/css/zurb_browser.css')
            add_stylesheet(req, 'theme/css/zurb_milestone.css')
            add_stylesheet(req, 'theme/css/zurb_tickets.css')
            add_script(req, 'theme/js/custom.modernizr.js')
            add_script(req, 'theme/js/foundation.min.js')
            #add_script(req, 'theme/js/jquery.js')
            #add_script(req, 'theme/js/zepto.js')
            #add_script(req, 'theme/js/jquery.js')

        if template is None and data is None and sys.exc_info() == (None, None, None):
            return template, data, content_type

        links = req.chrome.get('links',{})
        #replace favicon if appropriate
        if self.env.project_icon == 'common/trac.ico':
            bh_icon = 'theme/img/bh.ico'
            new_icon = {'href': req.href.chrome(bh_icon),
                        'type': get_mimetype(bh_icon)}
            if links.get('icon'):
                links.get('icon')[0].update(new_icon)
            if links.get('shortcut icon'):
                links.get('shortcut icon')[0].update(new_icon)

        if self.disable_all_trac_css and self.is_active_theme:
            if self.disable_all_trac_css:
                stylesheets = links.get('stylesheet',[])
                if stylesheets:
                    path = req.base_path + '/chrome/common/css/'
                    _iter = ([ss, ss.get('href', '')] for ss in stylesheets)
                    links['stylesheet'] = [ss for ss, href in _iter
                                           if not href.startswith(path) or
                                              href.rsplit('/', 1)[-1] in self.ZURB_KEEP_CSS]
            template, modifier = self.ZURB_TEMPLATE_MAP.get(
                template, (template, None))
            if modifier is not None:
                modifier = getattr(self, modifier)
                modifier(req, template, data, content_type, self.is_active_theme)

       # if is_active_theme and data is not None:
        #    data['responsive_layout'] = self.env.config.getbool(
         #       'bloodhound', 'responsive_layout', 'true')

        return template, data, content_type


        # ITemplateProvider methods


    def get_htdocs_dirs(self):
        """
        Return a list of directories with static resources (such as style
        sheets, images, etc.)
        Each item in the list must be a `(prefix, abspath)` tuple. The
        `prefix` part defines the path in the URL that requests to these
        resources are prefixed with.

        The `abspath` is the absolute path to the directory containing the
        resources on the local file system.
        """
        yield "zurbtheme", resource_filename(__name__, 'htdocs')

    def get_templates_dirs(self):
        """Return a list of directories containing the provided template
        files.
        """
        return []

    def _norm(self, req, template, data, content_type, is_active):
        """Insert roadmap.css
        """
        #add_stylesheet(req, 'dashboard/css/roadmap.css')
        return
