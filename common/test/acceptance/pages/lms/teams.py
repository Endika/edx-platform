# -*- coding: utf-8 -*-
"""
Teams pages.
"""

from .course_page import CoursePage
from ..common.paging import PaginatedUIMixin

from .fields import FieldsMixin


TOPIC_CARD_CSS = 'div.wrapper-card-core'
BROWSE_BUTTON_CSS = 'a.nav-item[data-index="1"]'
TEAMS_LINK_CSS = '.action-view'
TEAMS_HEADER_CSS = '.teams-header'
CREATE_TEAM_LINK_CSS = '.create-team'


class TeamsPage(CoursePage):
    """
    Teams page/tab.
    """
    url_path = "teams"

    def is_browser_on_page(self):
        """ Checks if teams page is being viewed """
        return self.q(css='body.view-teams').present

    def get_body_text(self):
        """ Returns the current dummy text. This will be changed once there is more content on the page. """
        main_page_content_css = '.page-content-main'
        self.wait_for(
            lambda: len(self.q(css=main_page_content_css).text) == 1,
            description="Body text is present"
        )
        return self.q(css=main_page_content_css).text[0]

    def browse_topics(self):
        """ View the Browse tab of the Teams page. """
        self.q(css=BROWSE_BUTTON_CSS).click()


class BrowseTopicsPage(CoursePage, PaginatedUIMixin):
    """
    The 'Browse' tab of the Teams page.
    """

    url_path = "teams/#browse"

    def is_browser_on_page(self):
        """Check if the Browse tab is being viewed."""
        button_classes = self.q(css=BROWSE_BUTTON_CSS).attrs('class')
        if len(button_classes) == 0:
            return False
        return 'is-active' in button_classes[0]

    @property
    def topic_cards(self):
        """Return a list of the topic cards present on the page."""
        return self.q(css=TOPIC_CARD_CSS).results

    def browse_teams_for_topic(self, topic_name):
        """
        Show the teams list for `topic_name`.
        """
        self.q(css=TEAMS_LINK_CSS).filter(
            text='View Teams in the {topic_name} Topic'.format(topic_name=topic_name)
        )[0].click()
        self.wait_for_ajax()


class BrowseTeamsPage(CoursePage, PaginatedUIMixin):
    """
    The paginated UI for browsing teams within a Topic on the Teams
    page.
    """
    def __init__(self, browser, course_id, topic):
        """
        Set up `self.url_path` on instantiation, since it dynamically
        reflects the current topic.  Note that `topic` is a dict
        representation of a topic following the same convention as a
        course module's topic.
        """
        super(BrowseTeamsPage, self).__init__(browser, course_id)
        self.topic = topic
        self.url_path = "teams/#topics/{topic_id}".format(topic_id=self.topic['id'])

    def is_browser_on_page(self):
        """Check if we're on the teams list page for a particular topic."""
        has_correct_url = self.url.endswith(self.url_path)
        teams_list_view_present = self.q(css='.teams-main').present
        return has_correct_url and teams_list_view_present

    @property
    def header_topic_name(self):
        """Get the topic name displayed by the page header"""
        return self.q(css=TEAMS_HEADER_CSS + ' .page-title')[0].text

    @property
    def header_topic_description(self):
        """Get the topic description displayed by the page header"""
        return self.q(css=TEAMS_HEADER_CSS + ' .page-description')[0].text

    @property
    def team_cards(self):
        """Get all the team cards on the page."""
        return self.q(css='.team-card')

    def create_team_link_present(self):
        """ Check if create team link is present."""
        return self.q(css=CREATE_TEAM_LINK_CSS).present

    def click_create_team_link(self):
        """ Click on create team link."""
        self.q(css=CREATE_TEAM_LINK_CSS).click()

    def search_team_link_present(self):
        """ Check if create team link is present."""
        return self.q(css='.search-team-descriptions').present

    def click_search_team_link(self):
        """ Click on create team link."""
        self.q(css='.search-team-descriptions').click()

    def browse_all_teams_link_present(self):
        """ Check if browse team link is present."""
        return self.q(css='.browse-teams').present

    def click_browse_all_teams_link(self):
        """ Click on browse team link."""
        self.q(css='.browse-teams').click()


class CreateTeamPage(CoursePage, FieldsMixin):
    """
    Create team page.
    """
    def __init__(self, browser, course_id, topic):
        """
        Set up `self.url_path` on instantiation, since it dynamically
        reflects the current topic.  Note that `topic` is a dict
        representation of a topic following the same convention as a
        course module's topic.
        """
        super(CreateTeamPage, self).__init__(browser, course_id)
        self.topic = topic
        # TODO update this when url get updated, currently no explicit url for creation page like others.
        self.url_path = "teams/#topics/{topic_id}".format(topic_id=self.topic['id'])

    def is_browser_on_page(self):
        """Check if we're on the create team page for a particular topic."""
        has_correct_url = self.url.endswith(self.url_path)
        teams_create_view_present = self.q(css='.create-new-team').present
        return has_correct_url and teams_create_view_present

    @property
    def header_page_name(self):
        """Get the page name displayed by the page header"""
        return self.q(css='.page-header .page-title')[0].text

    @property
    def header_page_description(self):
        """Get the page description displayed by the page header"""
        return self.q(css='.page-header .page-description')[0].text

    @property
    def header_page_breadcrumbs(self):
        """Get the page breadcrumb text displayed by the page header"""
        return self.q(css='.page-header .breadcrumbs')[0].text

    @property
    def validation_message_text(self):
        """Get the error message text"""
        return self.q(css='.wrapper-msg .copy')[0].text

    def create_team(self):
        """Click on create team button"""
        self.q(css='.create-team .action-primary').click()

    def cancel_team(self):
        """Click on cancel team button"""
        self.q(css='.create-team .action-cancel').click()
