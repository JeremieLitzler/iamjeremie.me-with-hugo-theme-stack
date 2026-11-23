# Research: commit message enforcement in Azure DevOps (fact check)

Article checked: `content/post/2026-11/enforcing-commit-message-standards-in-azure-devops/index.md`. Date of research: 2026-11-23. No existing research-note convention was found in the repo (only `docs/agents/` and `docs/adr/` conventions), so this file creates `docs/research/`. Snippets were run with Git for Windows 2.56.1 (GNU bash 5.3.15 as `sh`, GNU grep 3.0).

## What must change in the article (ranked)

- The second hook (`#id-type: msg`) is broken for the editor workflow: with plain `git commit` (message typed in the editor) Git strips lines starting with `#`, so the message becomes empty and the commit aborts with "Aborting commit due to empty commit message." It only works with `-m`/`-F`. Change the format (for example `feat(#1234): ...` or `1234-feat: ...`) or set `git config commit.cleanup whitespace`/`--cleanup=whitespace`, and say so.
- The first hook checks any line, not the subject: a message like `wip stuff` + blank line + body line `feat: some long description here` passes. Check only the first line (`head -n 1`) as the second hook does.
- The first hook rejects valid Conventional Commits: scope (`feat(auth): ...`), breaking marker (`feat!: ...`), and the types `perf`, `build`, `ci`, `revert`. Add an optional scope and `!` group and the missing types.
- The first hook rejects every merge, revert and fixup commit (`Merge branch ...`, `Revert "..."`, `fixup! ...`). Mention it or allow those prefixes.
- The first hook's `.{10,}` requires a description of at least 10 characters, so `feat: add login` is accepted but `feat: fix typo`-style short descriptions like `fix: typo` fail. Not an error per se, but the error message does not say so.
- The sentence "Anything that doesn't match the pattern will fail the `git commit -m` command" should say it applies to every way of committing (editor, `-m`, `-F`, merge) except `--no-verify`/`-n`.
- The claim "Azure DevOps Services (cloud) doesn't let you run custom server-side Git hooks" is consistent with every source found, but no first-party Microsoft page states it in so many words. Do not add that on-premises Azure DevOps Server supports custom hooks: no source supports it. Safer wording: "Azure Repos doesn't offer custom server-side Git hooks".
- Add the real server-side options: a branch policy with a build validation pipeline or a PR status check (custom status server) can validate commit messages after the push, at PR time. There is no built-in commit message format policy.
- State that `core.hooksPath` relative paths are relative to the directory where hooks run (the working tree root for `git commit`), and that it needs Git 2.9 or later.
- Minor: the second script's `\\(` inside double quotes is fine (shell turns it into `\(`), the `head -n 1` check is correct, but the error output echoes the full message and the emoji lines are cosmetic. The `exit 0` and trailing blank lines in the code blocks are harmless.

## Claim 1: Azure DevOps Services and Server and server-side hooks

Verdict for Services (cloud): Partly true, consistent with all evidence but not stated verbatim by Microsoft. Microsoft's documented extension points are branch policies, status checks and service hooks, and no page documents custom `pre-receive` or `update` hooks. A Microsoft Q&A question (2024-03-26) asking how to add a server-side `pre-receive` hook to Azure DevOps got no answer other than a redirect to other forums.

Verdict for Azure DevOps Server (on-premises): Could not verify that it supports them; the suspicion that the original claim is wrong is not contradicted. I found no Microsoft Learn page documenting custom `pre-receive`/`update` hooks in Azure DevOps Server, and the Azure Repos docs list no such feature for any version. A Microsoft Q&A answer on a related limitation (atomic push) reportedly says Azure DevOps runs a custom Git server and does not allow changing low-level server settings even on self-hosted installs; I did not open that page, so treat it as unconfirmed. The article should not claim on-premises supports custom hooks.

Note that Azure DevOps "service hooks" are different: they are HTTP notifications sent after events (push, PR created) and cannot reject a push. Git's own definition of the server-side hooks that would be needed: `pre-receive` runs once per push and "If the hook exits with non-zero status, none of the refs will be updated"; `update` runs per ref.

Sources:
- https://git-scm.com/docs/githooks (pre-receive, update)
- https://learn.microsoft.com/en-us/azure/devops/repos/git/create-pr-status-server?view=azure-devops (service hooks plus status API, applies to Services, Server and Server 2022)
- https://learn.microsoft.com/en-us/answers/questions/1632964/add-git-hooks-on-azure (unanswered hook question)
- https://learn.microsoft.com/en-us/answers/questions/1625996/can-we-implement-a-server-level-pre-commit-hook-to (no moderator answer; only the asker mentions SaaS repo policies and webhooks)

## Claim 2: native enforcement of commit message format in Azure Repos

Verdict: Confirmed that there is no native commit message format policy. What exists, per the repository settings page:
- Commit author email validation (blocks pushes whose author email does not match patterns; Server 2020.1 or later).
- File path validation (block pushes introducing matching paths; Server 2020.1 or later).
- Reserved names, maximum path length, maximum file size.
- Repo setting "Include PR ID in commit message" (affects PR completion commit titles, does not validate anything).
- Auto-linking of `#123` in commit messages to work items (a link feature, not validation).

Branch policies listed on the branch policy page: minimum reviewers, linked work items, comment resolution, merge types, build validation, status checks, automatic reviewers. None checks commit message content. The "linked work items" policy checks the PR, not commits.

Indirect options that do exist:
- Build validation: a pipeline runs for the PR and can run any script (for example `commitlint` over the PR's commits) and fail the PR. It runs at PR time, not at push time, so it cannot reject a push.
- Status checks: an external service receives PR service hook events and posts a status through the PR Status API, and a required status check blocks completion. Microsoft's Node.js sample checks the PR title for "WIP"; the same approach could check commit messages. This needs a hosted service.
- Marketplace extensions: I found no extension that enforces commit message format as a policy. The only commit-message validator found was a GitHub Action (joshjohanning/azdo_commit_message_validator) that checks for `AB#123` work item links, which is not Azure Repos native. Could not verify any Marketplace listing.

Sources:
- https://learn.microsoft.com/en-us/azure/devops/repos/git/repository-settings?view=azure-devops
- https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies?view=azure-devops (sections "Set build validation" and "Require status checks")
- https://learn.microsoft.com/en-us/azure/devops/repos/git/create-pr-status-server?view=azure-devops
- https://learn.microsoft.com/en-us/azure/devops/repos/git/pr-status-policy

## Claim 3: the `commit-msg` hook

Verdict: Confirmed for argument, exit status and `--no-verify`. Confirmed (by Git's design, and demonstrated) that `.git/hooks` is not versioned.
- githooks: "This hook is invoked by git-commit and git-merge, and can be bypassed with the `--no-verify` option. It takes a single parameter, the name of the file that holds the proposed commit log message. Exiting with a non-zero status causes the command to abort."
- git-commit: `-n`, `--no-verify` "Bypass the `pre-commit` and `commit-msg` hooks."
- Run result: `git commit -n -m 'bad'` succeeded with the hook active.
- Worth adding to the article: the hook also runs for `git merge`, which is why merge commit messages hit it. `.git/hooks` lives inside `.git`, which Git never tracks or clones (inferred from how Git works; no single doc sentence quoted).

Sources:
- https://git-scm.com/docs/githooks
- https://git-scm.com/docs/git-commit

## Claim 4: `core.hooksPath`

Verdict: Confirmed with a correction on relative paths.
- Introduced in Git 2.9: release notes 2.9.0 say "A new configuration variable core.hooksPath allows customizing where the hook directory is."
- git-config: "The path can be either absolute or relative. A relative path is taken as relative to the directory where the hooks are run (see the 'DESCRIPTION' section of githooks)." For `git commit` hooks run from the root of the working tree, so `.githooks` resolves to `<repo root>/.githooks`. Tested: committing from a subdirectory with `core.hooksPath .githooks` still ran the hook.
- Executable bit: githooks says "Hooks that don't have the executable bit set are ignored." The article's `chmod +x` step is right on Linux and macOS. On Windows, the test below was inconclusive: after `chmod -x` under Git for Windows 2.56.1 the commit still failed as if the hook ran. Could not verify the behaviour from documentation. Practical advice: commit the file with the executable bit recorded (`git update-index --chmod=+x .githooks/commit-msg`) so cloning on Linux or macOS keeps it, and Git for Windows runs hooks through its bundled sh using the shebang line.
- `git config core.hooksPath .githooks` without `--global` writes to the repository's local config (`.git/config`). Verified: `git config --show-origin core.hooksPath` printed `file:.git/config .githooks`. This is why each clone must run it once; the setting itself is not versioned.

Sources:
- https://git-scm.com/docs/git-config (core.hooksPath)
- https://git-scm.com/docs/githooks
- https://raw.githubusercontent.com/git/git/master/Documentation/RelNotes/2.9.0.adoc

## Claim 5: Conventional Commits and the type list

Verdict: Partly true. The article's list is a valid subset, but it is incomplete and does not allow scope or `!`.
- Spec 1.0.0: only `feat` and `fix` are mandated (rules 2 and 3: "The type `feat` MUST be used when a commit adds a new feature", "The type `fix` MUST be used when a commit represents a bug fix").
- Rule 14: "Types other than `feat` and `fix` MAY be used in your commit messages, e.g., docs: update ref docs."
- The spec summary credits the Angular convention for `build:`, `chore:`, `ci:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`. The article's list lacks `build`, `ci`, `perf`, and `revert` (the last one comes from the Angular/commitlint conventions, not named in the spec).
- Format: `<type>[optional scope][optional !]: <description>`, body one blank line after the description, footers after another blank line. Scope is "a noun describing a section of the codebase surrounded by parenthesis". Breaking change: `!` immediately before the colon, or a `BREAKING CHANGE:` footer.
- Rule 15: types are not case-sensitive, so `Feat:` is valid under the spec but rejected by the hook (the hook is stricter than the spec; fine if intended).
- Suggested regex for the first line: `^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9._/-]+\))?!?: .{10,}$`.

Sources:
- https://www.conventionalcommits.org/en/v1.0.0/

## Claim 6: correctness of the two hook scripts

### Script A, `^(feat|fix|docs|style|refactor|test|chore): .{10,}$`

Verdict: Partly true. It works for single-line messages of the listed types, but:
- Multi-line messages: `echo "$commit_msg" | grep -qE` matches per line, so the check passes if any line matches, not only the subject. Demonstrated: `wip stuff`, blank line, `feat: some long description here` passes (exit 0). Conversely a valid subject followed by any body passes too, which is the intended behaviour, but a bad subject can slip through.
- Scope: `feat(auth): add login flow` is rejected (exit 1).
- Breaking `!`: `feat!: drop node 6 support` is rejected.
- Merge, revert, fixup: `Merge branch x into main`, `Revert "feat: ..."`, `fixup! feat: ...` are all rejected.
- Case: `Feat: add user login` is rejected.
- `$(cat "$1")` strips trailing newlines, so a trailing blank line does not matter.
- The error text never explains the 10-character minimum.

### Script B, `^#[0-9]+-[a-z]+(\\([a-zA-Z0-9_-]+\\))?: .{1,34}$` in double quotes

Verdict: Confirmed for the regex and the subject-only check; Refuted as a usable format with the editor.
- Inside double quotes, sh turns `\\` into `\`, so grep receives `^#[0-9]+-[a-z]+(\([a-zA-Z0-9_-]+\))?: .{1,34}$`. Printed from the run: `PATTERN=[^#[0-9]+-[a-z]+(\([a-zA-Z0-9_-]+\))?: .{1,34}$]`. In ERE `\(` is a literal parenthesis and the bare parentheses form the optional group, so the scope works.
- `echo ... | head -n 1 | grep -qE` checks only the first line; a body is accepted.
- All three article examples match (table below). The 34-character limit applies to everything after `: ` (the description), not to the whole subject. The comment in the script says "[message <= 34 chars]", which is consistent; the "Rules" text "Message must be 1-34 characters long" is also consistent.
- Not matched: `#12-feat!: breaking` (no `!` support), hyphenated types, uppercase types. Fine if intended.
- The `#` problem. git-commit `--cleanup`: `strip` removes "commentary", and the default mode is "Same as `strip` if the message is to be edited. Otherwise `whitespace`." (`whitespace`: "Same as strip except #commentary is not removed"). Therefore with `git commit` (editor) a first line starting with `#1234-feat: ...` is treated as a comment and removed, leaving an empty message. Reproduced: hook passed, then Git printed "Aborting commit due to empty commit message." With `git commit -m '#1234-feat: add user login'` and `git commit -F file`, the default cleanup is `whitespace`, so the line is kept and the commit succeeded. The article's closing text ("will fail the `git commit -m` command") hides this because `-m` is the one case that works. Workarounds: start the message with the id elsewhere (for example `feat(#1234): add user login`, which also matches Azure Boards `#1234` linking anywhere in the message), or tell developers to set `git config commit.cleanup whitespace` (the git-commit page says `commit.cleanup` can change the default), or change `core.commentChar`.
- Order of events seen in the run: the hook ran and accepted the message file containing the `#` line, then Git cleaned it up. So the hook cannot detect the problem.
- The error output `echo "  $commit_msg"` prints the whole message including body; harmless, but with the editor the `# Please enter...` comment lines are not in the file seen by the hook after cleanup in this Git version, so nothing noisy appeared in the test.

Sources:
- https://git-scm.com/docs/git-commit (`--cleanup`, `--no-verify`, `commit.cleanup`)
- https://git-scm.com/docs/githooks

### Snippet test results

Run with `sh script message_file`; exit 0 means the message is accepted.

| Script | Message | Exit | Result |
| --- | --- | --- | --- |
| A | `feat: add user login` | 0 | accepted |
| A | `feat: short` | 1 | rejected (description under 10 chars) |
| A | `feat(auth): add login flow` | 1 | rejected, scope unsupported |
| A | `feat!: drop node 6 support` | 1 | rejected, `!` unsupported |
| A | `feat: add user login` + blank + body + footer | 0 | accepted |
| A | `perf: speed up the query loop` | 1 | rejected, type missing |
| A | `Merge branch x into main` | 1 | rejected |
| A | `Revert "feat: add user login"` | 1 | rejected |
| A | `fixup! feat: add user login` | 1 | rejected |
| A | `Feat: add user login` | 1 | rejected, case |
| A | `wip stuff` + blank + `feat: some long description here` | 0 | accepted wrongly (any-line match) |
| B | `#1234-feat: add user login` | 0 | accepted |
| B | `#5678-fix(auth): resolve token issue` | 0 | accepted |
| B | `#9012-docs: update README` | 0 | accepted |
| B | `#1-feat: this subject line is longer than thirty-four chars` | 1 | rejected (over 34) |
| B | `#12-feat: add login` + blank + `body line` | 0 | accepted, only subject checked |
| B | `#12-feat!: breaking` | 1 | rejected |
| B | `#12-feat-x: a` | 1 | rejected |
| B | `#12-Feat: a` | 1 | rejected |
| B in git, `git commit -m '#1234-feat: add user login'` | | commit created | works |
| B in git, `git commit -F file` with `#1234-feat: add via file` | | commit created | works |
| B in git, plain `git commit` with the message typed in the editor as `#1234-feat: via editor` | | "Aborting commit due to empty commit message." | fails, `#` line stripped by `--cleanup=strip` |
| B in git, `git commit -n -m 'bad'` | | commit created | hook bypassed |
| B in git, bad message from a subdirectory with `core.hooksPath .githooks` | | blocked | relative path resolved from the repo root |
| B in git, after `chmod -x` on the hook (Windows) | | blocked | inconclusive on exec bit under Git for Windows |
