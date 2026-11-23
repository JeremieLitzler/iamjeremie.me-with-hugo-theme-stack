# Brief: corrections for "Enforcing Commit Message Standards in Azure DevOps"

Source of the findings: `docs/research/commit-message-enforcement-azure-devops.md`. Article: `content/post/2026-11/enforcing-commit-message-standards-in-azure-devops/index.md`. Branch: `docs/proof-commit-message-article`.

## Corrections the article needs

### 1. The `#id-type:` format breaks in the editor

It only works with `git commit -m` or `-F`. With a plain `git commit`, Git's default cleanup (`--cleanup=strip`) removes lines starting with `#`. The hook accepts the message, then Git aborts with "Aborting commit due to empty commit message." The research agent reproduced this. Fixes: use `feat(#1234): ...`, or set `commit.cleanup whitespace`.

Your comment: This is what the team does, but this is a good note to add.

### 2. The first script is too loose and too strict

It matches any line of the message, not just the subject: `wip stuff`, a blank line, then `feat: some long description here` passes. It rejects `feat(auth): ...` and `feat!: ...`. It rejects the types `perf`, `build`, `ci` and `revert`, and merge, revert and fixup commits. The Conventional Commits spec only mandates `feat` and `fix`; the other types come from convention.

Your comment: update regex to be more faithful to Conventional Commits spec

### 3. The server-side hooks claim can't be verified

No Microsoft Learn page says Azure DevOps Server supports custom `pre-receive` or `update` hooks. No page says outright that Azure DevOps Services lacks them either; the evidence is indirect. Safest wording: "Azure Repos doesn't offer custom server-side hooks", with no on-premises claim. The current line 21 of the article is stronger than that.

Your comment: use safest wording

### 4. Azure Repos has no native commit-message policy

Its push policies cover author email, file path, reserved names, path length and file size. Alternatives worth adding to the article: build validation (a pipeline script at PR time) or a PR status check. No Marketplace extension was found that does this.

Your comment: go for adding alternative suggestion

## Confirmed, no change needed

- The `commit-msg` hook takes one argument, the path to the message file. A non-zero exit aborts the commit. `-n` and `--no-verify` bypass it. It also runs for `git merge`.
- `core.hooksPath` arrived in Git 2.9. Relative paths resolve from the repo root for commits. Without `--global`, it writes to `.git/config`. Git docs say hooks without the executable bit are ignored; the `chmod -x` test on Windows was inconclusive.
- The second script's regex is fine: the shell turns `\\(` into `\(`, all three article examples match, and `head -n 1` checks only the subject. The 34-character limit applies to the description after `: `, not the whole subject.

## Not verified

The Microsoft Q&A claim that Azure DevOps Server disallows low-level Git server settings (atomic-push thread) was seen only in search results. The research file flags it as unconfirmed.

Your comment: remove claim then

## Questions

### 1. Article edits: which corrections should be applied to `index.md`?

- a. All four.
- b. Only some (name the numbers in your comment).
- c. None, I will edit it myself.

Your answer: A

### 2. The `#id-type:` format (correction 1): how should the article handle it?

- a. Switch the examples and the regex to `feat(#1234): ...`.
- b. Keep the `#1234-feat:` format and add a warning about `-m` versus the editor, with the `commit.cleanup whitespace` workaround.
- c. Keep it as is.

Your answer: B

### 3. Research file `docs/research/commit-message-enforcement-azure-devops.md`: what should happen to it?

- a. Keep it in the branch so it is committed with the article.
- b. Delete it after the article is fixed.

Your answer: A

### 4. This brief (`docs/research/brief.md`): what should happen to it?

- a. Delete it once your answers are applied.
- b. Keep it in the branch.

Your answer: B
