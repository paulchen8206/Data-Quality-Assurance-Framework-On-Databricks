# GitHub Repository Configuration Guide

This guide provides instructions for configuring GitHub Topics/Tags and Branch Protection Rules for the QA Framework repository.

## 📌 GitHub Topics/Tags for Discoverability

GitHub Topics help users discover your repository. Add these via the GitHub web interface.

### How to Add Topics

1. Go to **https://github.com/paulchen8206/Qa-Framework-On-Databricks**
2. Click the **⚙️ gear icon** next to "About" (top right of page)
3. In the "Topics" field, add these suggested topics:
   - `databricks`
   - `data-quality`
   - `data-validation`
   - `python`
   - `pyspark`
   - `great-expectations`
   - `quality-assurance`
   - `testing-framework`
   - `data-engineering`
   - `databricks-bundle`
   - `pytest`
   - `spark`
4. Click **Save changes**

### Recommended Topics Priority

**Essential (High Discoverability):**
- `databricks`
- `data-quality`
- `python`
- `pyspark`

**Important (Relevant):**
- `data-validation`
- `great-expectations`
- `testing-framework`
- `data-engineering`

**Nice to Have:**
- `quality-assurance`
- `databricks-bundle`
- `pytest`
- `spark`

### Also Update Repository Description

In the same "About" section, add this description:
```
Production-ready Data Quality Assurance Framework for Databricks with Python. Features DataValidator for quick checks and Great Expectations integration for comprehensive validation pipelines.
```

And add the website field (if you have documentation):
```
https://github.com/paulchen8206/Qa-Framework-On-Databricks
```

---

## 🔒 Branch Protection Rules

Branch protection rules prevent force pushes, require reviews, and ensure code quality before merging.

### How to Set Up Branch Protection

1. Go to **https://github.com/paulchen8206/Qa-Framework-On-Databricks/settings/branches**
2. Click **Add rule** or **Add branch protection rule**
3. In "Branch name pattern", enter: `main`

### Recommended Protection Settings

#### Basic Protection (Recommended for Solo/Small Teams)

✅ Check these options:

- **Require a pull request before merging**
  - Required approvals: 0 or 1 (your choice)
  - Dismiss stale pull request approvals when new commits are pushed
  
- **Require status checks to pass before merging**
  - Require branches to be up to date before merging
  - Status checks to require (after first CI run):
    - `test`
    - `lint` (optional)
    - `validate-bundle` (optional)

- **Require conversation resolution before merging**
  - Ensures all PR comments are addressed

- **Do not allow bypassing the above settings**
  - Applies rules even to administrators

#### Advanced Protection (For Teams)

Additional options to consider:

- **Require signed commits** (for security)
- **Require linear history** (cleaner git history)
- **Require deployments to succeed** (if using CD)
- **Lock branch** (for archived/stable branches only)

#### Example Configuration Steps

```
1. Branch name pattern: main
2. ✅ Require a pull request before merging
   - Required number of approvals: 1
   - ✅ Dismiss stale pull request approvals
   - ✅ Require review from Code Owners (if CODEOWNERS file exists)
3. ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - Search and select: test, lint, build
4. ✅ Require conversation resolution before merging
5. ✅ Include administrators
6. Click "Create" or "Save changes"
```

### For Development Branch (Optional)

If you create a `develop` branch for ongoing development:

1. Create another protection rule
2. Branch name pattern: `develop`
3. Use lighter protection:
   - Require PRs: Yes
   - Required approvals: 0
   - Status checks: Optional

### Testing Branch Protection

After setting up:

1. Try to push directly to `main`:
   ```bash
   git checkout main
   echo "test" >> test.txt
   git add test.txt
   git commit -m "test"
   git push  # This should be blocked!
   ```
   
2. You should see an error like:
   ```
   remote: error: GH006: Protected branch update failed
   ```

3. The correct workflow now requires:
   ```bash
   git checkout -b feature/my-change
   # Make changes
   git commit -m "feat: my change"
   git push origin feature/my-change
   # Then create PR on GitHub
   ```

---

## 🤖 CI/CD Status Checks

After the first GitHub Actions run completes, you can require specific checks to pass:

### Available Status Checks (from `.github/workflows/ci-cd.yml`)

1. **test** - Runs pytest on multiple Python versions
2. **lint** - Code quality checks
3. **validate-bundle** - Validates Databricks bundle
4. **build** - Builds the package

### How to Require Status Checks

1. Go to branch protection rules
2. Check "Require status checks to pass before merging"
3. After first workflow run, search for checks by name
4. Select the checks you want to require
5. Save changes

---

## 📊 Additional Repository Settings

### Enable Security Features

1. Go to **Settings** → **Security & analysis**
2. Enable:
   - ✅ Dependency graph
   - ✅ Dependabot alerts
   - ✅ Dependabot security updates
   - ✅ Secret scanning (if available)

### Configure Insights

1. **Pulse** - View recent activity
2. **Contributors** - See contribution stats
3. **Traffic** - Monitor views and clones
4. **Insights** - Access analytics

### Social Preview Image (Optional)

1. Go to **Settings** → **General**
2. Scroll to "Social preview"
3. Upload an image (1280x640px recommended)
4. This appears when sharing links on social media

---

## ✅ Verification Checklist

After completing the setup, verify:

- [ ] Topics/tags added and visible on repo page
- [ ] Repository description updated
- [ ] Branch protection enabled for `main`
- [ ] CI/CD workflow runs successfully
- [ ] Status checks configured (after first run)
- [ ] Security features enabled
- [ ] Direct pushes to `main` are blocked
- [ ] PR workflow works correctly

---

## 📚 Additional Resources

- [GitHub Docs - Managing Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub Docs - Classifying Your Repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Note**: These settings can be adjusted over time based on your team's needs and workflow preferences.
