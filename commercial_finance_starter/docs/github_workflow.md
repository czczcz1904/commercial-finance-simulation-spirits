# GitHub workflow: publish your own contribution

The goal is to maintain a transparent project history that shows your real work. Do not manufacture commits or claim generated data as real company data. The generator is a starting point; your data checks, Power Query transformations, DAX measures, dashboard design and business commentary should be your own reviewed contributions.

## 1. Create the repository

1. Sign in to GitHub and select **New repository**.
2. Use a descriptive name such as `commercial-finance-simulation-vietnam-spirits`.
3. Set it to **Public** only if you are comfortable sharing the code and synthetic data; otherwise start as Private.
4. Do not initialize with a second README if you already have this starter README locally.
5. Copy the repository's HTTPS URL.

## 2. Open the project locally

Extract the starter ZIP, open the extracted folder in VS Code, then open **Terminal → New Terminal** at the project root.

Check that Python is installed:

```bash
python --version
```

Generate data and check the report:

```bash
python scripts/generate_data.py
```

## 3. Initialize Git and make your first commit

```bash
git init
git branch -M main
git add README.md .gitignore scripts docs data
git status
git commit -m "chore: initialize commercial finance simulation"
```

If Git asks for your identity, set the name and email you want associated with your commits:

```bash
git config --global user.name "Your GitHub Name"
git config --global user.email "your-verified-github-email@example.com"
```

Use an email verified on your GitHub account, or GitHub's provided `noreply` email if you prefer not to expose your personal email. Then repeat the commit if it did not complete.

## 4. Connect and push to GitHub

Replace the URL below with the HTTPS URL for your repository:

```bash
git remote add origin https://github.com/YOUR-USERNAME/commercial-finance-simulation-vietnam-spirits.git
git push -u origin main
```

GitHub may prompt you to authenticate in a browser or through Git Credential Manager. Do not put a password or personal access token directly into the remote URL or commit it to the repository.

## 5. Make meaningful commits as you do the work

A good project history could look like this (only make a commit after you have actually completed the work):

```bash
git add docs/data_dictionary.md
git commit -m "docs: define fact table grain and KPI assumptions"

git add excel/
git commit -m "analysis: add source data reconciliation workbook"

git add powerbi/
git commit -m "feat: build commercial performance dashboard"

git add presentation/ screenshots/ README.md
git commit -m "docs: publish commercial insights and dashboard walkthrough"

git push
```

Do not create empty commits simply to fill the contribution graph. Commits should correspond to real, reviewable changes. GitHub generally attributes commits to your account when the commit email is linked to that account; contribution-graph visibility also depends on repository and contribution settings.

## 6. Make the work easy to review

- Add screenshots of the final dashboard to `screenshots/` and embed them in README.
- Add a one-page executive summary to `presentation/`.
- Keep data lineage, synthetic-data disclaimer and limitations visible.
- Write a concise `Key findings` section with three evidence-backed insights and the actions you recommend.
- Pin the repository to your GitHub profile after it is polished.

## 7. Before making the repository public

- Confirm there are no personal files, credentials, API keys, access tokens or private company data.
- Confirm every dataset is synthetic or has a documented public source and collection date.
- Do not use Pernod Ricard's logo or imply affiliation, employment or access to internal systems.
- Avoid committing temporary files such as `.pbix` backups, cache files or local environment folders.
