# Copy and paste this into your own MAESTRO terminal in Maestri

Create an isolated Instagram Social Agent workspace for this computer, without modifying existing workspaces.

1. Read the local installation folder at %USERPROFILE%\InstagramSocialAgent, including INSTRUCOES-AGENTE.md and MAESTRI-BOOTSTRAP.md. Do not read any other personal directories.
2. Verify that the current Maestri session is Maestro-enabled using 'maestri list' and 'maestri recruit --help'. If recruitment is unavailable, explain what the user must enable; do not fake success.
3. Ask which provider they wish to use: Codex, Claude Code or Antigravity, and check their available configured presets. Do not select another person's accounts.
4. Using the native 'maestri recruit' command, recruit up to three new agents in the user's OWN workspace, working directory %USERPROFILE%\InstagramSocialAgent:
   - Social Research: runs discover.cmd for a user-chosen niche and region, documents sources and deduplicates candidates.
   - Social CRM: runs social.cmd and service.cmd, prepares editable personalized message drafts, and summarizes reports.
   - Social Browser: uses the native 'maestri portal create https://www.instagram.com/ "My Instagram"' browser portal. Ask the user to log in manually. Never ask for passwords or 2FA codes.
5. Ensure all work uses only the data subfolder under this installation. Never connect any publisher databases, external workspaces, accounts, terminals, cookies or API secrets.
6. Ask the user to choose their company, niche, geographic region and message template; write their config locally with service.cmd setup. The user can optionally provide their OWN public search API key for discovery.
7. If they want official Instagram messaging, guide them through creating their OWN Meta developer application, permissions and HTTPS webhook. Do not claim this setup is complete until actual API verification succeeds.
8. Run a local read-only smoke test using service.cmd status, social.cmd draft, and discover.cmd --help. Verify successful terminal creation with 'maestri list'. Report precise results.
9. Do not follow profiles or send unsolicited cold Directs automatically. Any outbound official API replies require eligible conversations and explicitly approved messages.
10. Do not install paid products, alter credentials, delete files, import browser profiles, or modify any existing Maestri terminals.

Explain any unsupported operation instead of silently skipping it. Show a brief summary of what was actually installed and verified.
