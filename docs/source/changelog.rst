Changelog
=========

Version 0.1.0 (2026-07-15)
---------------------------

Features
^^^^^^^^

- Added **context manager** support (``with`` statement) for safe file handling.
- Added **batch processing** capability to parse all cookie files in a directory (``-d/--directory`` CLI flag).
- Added **cookie summary statistics** with ``--summary`` CLI flag, showing total cookies, unique domains, flag distribution, and top domains.
- Added ``summarize_cookies()`` static method for programmatic summary generation.
- Added ``batch_process()`` static method for programmatic directory processing.

CI/CD & Distribution
^^^^^^^^^^^^^^^^^^^^

- Added GitHub Actions CI workflow (``test.yml``) — automated testing on push/PR to ``main`` across Python 3.10–3.13.
- Added GitHub Actions CD workflow (``publish.yml``) — automated PyPI publishing via OIDC Trusted Publishing on GitHub Release.
- Added ``Dockerfile`` with multi-stage build for containerized usage.
- Added ``docker-compose.yml`` for easy container orchestration.

Testing
^^^^^^^

- Implemented ``test_read_page_sizes`` (previously empty).
- Added ``test_write_results_json``, ``test_write_results_csv``, ``test_write_results_txt`` for output validation.
- Added ``test_write_results_invalid_type`` for unsupported output format handling.
- Added ``test_context_manager`` and ``test_context_manager_invalid_file``.
- Added ``test_summarize_cookies``, ``test_summarize_cookies_empty``, ``test_summarize_cookies_none``, ``test_summarize_cookies_same_domain``.
- Added ``test_batch_processing``, ``test_batch_processing_empty_directory``, ``test_batch_processing_invalid_directory``, ``test_batch_processing_mixed_files``.
- Added ``test_open_file_ioerror`` and ``test_read_cookie_file_no_file_opened``.

Documentation
^^^^^^^^^^^^^

- Upgraded Sphinx theme to ``sphinx_rtd_theme`` for modern ReadTheDocs styling.
- Added ``sphinx.ext.viewcode`` and ``sphinx.ext.napoleon`` extensions.
- Added ``.readthedocs.yaml`` configuration for automated documentation builds.
- Added this changelog page.

Version 0.0.1
-------------

- Initial release with binary cookie file parsing.
- Support for JSON, CSV, and TXT output formats.
- Command-line interface with ``-i``, ``-t``, and ``-o`` options.
