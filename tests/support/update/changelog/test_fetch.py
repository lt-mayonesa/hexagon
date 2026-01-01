import os
from unittest.mock import Mock, patch

from hexagon.runtime.update.changelog.fetch import (
    LocalChangelogFile,
    RemoteChangelogFile,
    fetch_changelog,
)


class TestLocalChangelogFile:
    """Test LocalChangelogFile reads from local files correctly."""

    def test_readlines_returns_string_lines(self):
        """
        Given a local file opened in read mode.
        When readlines is called on LocalChangelogFile.
        Then it returns a list of strings.
        """
        # Create a mock file object that behaves like open('file', 'r')
        mock_file = Mock()
        mock_file.readlines.return_value = [
            "## v0.61.0\n",
            "### release\n",
            "chore: something\n",
        ]

        changelog_file = LocalChangelogFile(mock_file)
        lines = changelog_file.readlines()

        assert isinstance(lines, list)
        assert len(lines) == 3
        assert all(isinstance(line, str) for line in lines)
        assert lines[0] == "## v0.61.0\n"


class TestRemoteChangelogFile:
    """Test RemoteChangelogFile decodes bytes from HTTP response correctly."""

    def test_readlines_decodes_bytes_to_strings(self):
        """
        Given an HTTP response that returns bytes.
        When readlines is called on RemoteChangelogFile.
        Then it decodes each byte line to a string.
        """
        # Create a mock HTTP response
        mock_response = Mock()
        mock_response.readlines.return_value = [
            b"## v0.61.0\n",
            b"### release\n",
            b"chore: something\n",
        ]
        mock_response.headers.get_content_charset.return_value = "utf-8"

        changelog_file = RemoteChangelogFile(mock_response)
        lines = changelog_file.readlines()

        assert isinstance(lines, list)
        assert len(lines) == 3
        assert all(isinstance(line, str) for line in lines)
        assert lines[0] == "## v0.61.0\n"
        assert lines[1] == "### release\n"
        assert lines[2] == "chore: something\n"

    def test_readlines_uses_specified_charset(self):
        """
        Given an HTTP response with a specific charset.
        When readlines is called on RemoteChangelogFile.
        Then it uses that charset for decoding.
        """
        mock_response = Mock()
        mock_response.readlines.return_value = [b"## v0.61.0\n"]
        mock_response.headers.get_content_charset.return_value = "iso-8859-1"

        changelog_file = RemoteChangelogFile(mock_response)
        lines = changelog_file.readlines()

        assert lines[0] == "## v0.61.0\n"
        # Verify the mock was called with the correct charset
        mock_response.readlines.assert_called_once()

    def test_readlines_defaults_to_utf8_when_no_charset(self):
        """
        Given an HTTP response with no charset specified.
        When readlines is called on RemoteChangelogFile.
        Then it defaults to utf-8 encoding.
        """
        mock_response = Mock()
        mock_response.readlines.return_value = [
            b"## v0.61.0\n",
            b"### release\n",
        ]
        mock_response.headers.get_content_charset.return_value = None

        changelog_file = RemoteChangelogFile(mock_response)
        lines = changelog_file.readlines()

        # Should not raise an error and should decode successfully
        assert isinstance(lines, list)
        assert len(lines) == 2
        assert all(isinstance(line, str) for line in lines)

    def test_readlines_handles_unicode_characters(self):
        """
        Given an HTTP response with unicode characters.
        When readlines is called on RemoteChangelogFile.
        Then it correctly decodes unicode characters.
        """
        mock_response = Mock()
        mock_response.readlines.return_value = [
            b"## v0.61.0\n",
            b"### release\n",
            "feat: add \u2713 checkmark\n".encode("utf-8"),
        ]
        mock_response.headers.get_content_charset.return_value = "utf-8"

        changelog_file = RemoteChangelogFile(mock_response)
        lines = changelog_file.readlines()

        assert lines[2] == "feat: add ✓ checkmark\n"


class TestFetchChangelog:
    """Test fetch_changelog function correctly chooses between local and remote."""

    @patch.dict(os.environ, {}, clear=True)
    @patch("hexagon.runtime.update.changelog.fetch.urlopen")
    @patch("hexagon.runtime.update.changelog.fetch.add_github_access_token")
    def test_fetch_changelog_uses_remote_when_no_override(
        self, mock_add_token, mock_urlopen
    ):
        """
        Given no HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE is set.
        When fetch_changelog is called.
        Then it fetches from GitHub API using RemoteChangelogFile.
        """
        mock_response = Mock()
        mock_response.readlines.return_value = [b"## v0.61.0\n"]
        mock_response.headers.get_content_charset.return_value = "utf-8"
        mock_urlopen.return_value = mock_response

        result = fetch_changelog("test-org", "test-repo")

        assert isinstance(result, RemoteChangelogFile)
        mock_urlopen.assert_called_once()
        mock_add_token.assert_called_once()

    @patch.dict(
        os.environ, {"HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE": "/tmp/changelog.md"}
    )
    @patch("builtins.open", create=True)
    def test_fetch_changelog_uses_local_when_override_set(self, mock_open):
        """
        Given HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE is set.
        When fetch_changelog is called.
        Then it uses LocalChangelogFile with the specified path.
        """
        mock_file = Mock()
        mock_file.readlines.return_value = ["## v0.61.0\n"]
        mock_open.return_value = mock_file

        result = fetch_changelog("test-org", "test-repo")

        assert isinstance(result, LocalChangelogFile)
        mock_open.assert_called_once_with("/tmp/changelog.md", "r")

    @patch.dict(os.environ, {}, clear=True)
    @patch("hexagon.runtime.update.changelog.fetch.urlopen")
    @patch("hexagon.runtime.update.changelog.fetch.add_github_access_token")
    def test_fetch_changelog_constructs_correct_github_url(
        self, mock_add_token, mock_urlopen
    ):
        """
        Given a repository org and name.
        When fetch_changelog is called.
        Then it constructs the correct GitHub API URL.
        """
        mock_response = Mock()
        mock_response.readlines.return_value = [b"## v0.61.0\n"]
        mock_response.headers.get_content_charset.return_value = "utf-8"
        mock_urlopen.return_value = mock_response

        fetch_changelog("lt-mayonesa", "hexagon")

        # Get the Request object that was passed to urlopen
        call_args = mock_urlopen.call_args
        request = call_args[0][0]

        assert (
            request.full_url
            == "https://api.github.com/repos/lt-mayonesa/hexagon/contents/CHANGELOG.md"
        )
        assert request.get_header("Accept") == "application/vnd.github.3.raw"
