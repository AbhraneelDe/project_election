"""
assistant/constants.py
──────────────────────
Static data and strings for the Election Process Assistant.
"""

TIMELINE_STEPS = [
    {
        "phase": "Phase 1",
        "title": "Voter Registration",
        "icon": "📋",
        "period": "Months Before Election",
        "description": "Citizens register to vote with their local election authority. Deadlines vary by state — typically 15 to 30 days before Election Day.",
        "key_actions": ["Check eligibility", "Register at vote.gov", "Confirm registration status"],
    },
    {
        "phase": "Phase 2",
        "title": "Primary Elections",
        "icon": "🗳️",
        "period": "Spring Before General Election",
        "description": "Political parties hold primaries or caucuses to select their candidates for the general election. Voters choose among candidates within their party.",
        "key_actions": ["Know your party's primary date", "Review candidate platforms", "Cast your primary ballot"],
    },
    {
        "phase": "Phase 3",
        "title": "Campaigns & Debates",
        "icon": "📣",
        "period": "Summer – Fall",
        "description": "Nominated candidates campaign across the country, participate in presidential debates, and make their case to voters.",
        "key_actions": ["Watch official debates", "Research candidate positions", "Evaluate platforms objectively"],
    },
    {
        "phase": "Phase 4",
        "title": "Election Day",
        "icon": "🏛️",
        "period": "First Tuesday After First Monday in November",
        "description": "Citizens cast their votes at polling locations or via absentee/mail-in ballots. Polls open and close at state-designated times.",
        "key_actions": ["Bring valid ID", "Find your polling place", "Know your voting rights"],
    },
    {
        "phase": "Phase 5",
        "title": "Vote Counting & Certification",
        "icon": "📊",
        "period": "Days to Weeks After Election Day",
        "description": "Election officials count all ballots — including mail-in and provisional — and certify results. Recounts may occur in close races.",
        "key_actions": ["Follow official results", "Understand the certification process", "Know recount triggers"],
    },
    {
        "phase": "Phase 6",
        "title": "Electoral College",
        "icon": "🗺️",
        "period": "Mid-December",
        "description": "Electors from each state meet to cast their official electoral votes for President and Vice President based on their state's popular vote.",
        "key_actions": ["Understand the Electoral College", "Track electoral vote counts", "Learn about faithless electors"],
    },
    {
        "phase": "Phase 7",
        "title": "Congressional Certification",
        "icon": "📜",
        "period": "Early January",
        "description": "Congress officially counts and certifies the Electoral College votes in a joint session, confirming the President-elect.",
        "key_actions": ["Follow the joint session", "Understand the certification role", "Know objection procedures"],
    },
    {
        "phase": "Phase 8",
        "title": "Inauguration",
        "icon": "🎉",
        "period": "January 20th",
        "description": "The President-elect is sworn into office in the Inauguration ceremony at the US Capitol, officially beginning their term.",
        "key_actions": ["Watch the inauguration", "Learn about the oath of office", "Understand the transition of power"],
    },
]

SUGGESTED_QUESTIONS = [
    "How do I register to vote?",
    "What is the Electoral College?",
    "When is Election Day?",
    "How are votes counted?",
    "What ID do I need to vote?",
    "What is a primary election?",
    "How does mail-in voting work?",
    "Who certifies election results?",
]

# ── Fallback Response Templates ──────────────────────────────────────────────

FALLBACK_RESPONSES = {
    "registration": (
        "**Voter Registration**\n\n"
        "To register to vote in the United States:\n\n"
        "1. **Check eligibility**: You must be a US citizen, at least 18 years old (in most states), and a resident of the state.\n"
        "2. **Register online**: Visit **vote.gov** to register online or find your state's registration portal.\n"
        "3. **Register by mail**: Download and mail a National Voter Registration Form.\n"
        "4. **Register in person**: Visit your local election office, DMV, or public library.\n"
        "5. **Check the deadline**: Most states require registration 15–30 days before Election Day.\n\n"
        "Is there a specific state you'd like information about, or any step you'd like me to explain further?"
    ),
    "electoral_college": (
        "**The Electoral College**\n\n"
        "The Electoral College is the formal process by which the President and Vice President of the United States are elected:\n\n"
        "1. **538 total electors** — distributed among states based on congressional representation.\n"
        "2. **270 electoral votes** are needed to win the presidency.\n"
        "3. **Winner-take-all** — most states award all their electoral votes to the candidate who wins the state's popular vote.\n"
        "4. **Electors meet in December** in their respective state capitals to cast official votes.\n"
        "5. **Congress certifies** the electoral votes in early January.\n\n"
        "Is there a specific part of the Electoral College you'd like me to explain further?"
    ),
    "primaries": (
        "**Primary Elections & Caucuses**\n\n"
        "Primary elections and caucuses are how political parties select their candidates:\n\n"
        "1. **Primary elections**: Voters cast secret ballots to choose their preferred candidate within a party.\n"
        "2. **Caucuses**: Voters gather in public meetings and openly declare their preferences through discussion.\n"
        "3. **Open vs. closed primaries**: Some states allow any registered voter; others restrict voting to party members.\n"
        "4. **Delegates**: Primary winners earn delegates who will officially nominate the candidate at the party convention.\n\n"
        "Is there anything specific about primaries you'd like to know?"
    ),
    "counting": (
        "**Vote Counting & Certification**\n\n"
        "After Election Day, votes go through a rigorous counting and verification process:\n\n"
        "1. **Initial count**: Election workers count all in-person ballots on election night.\n"
        "2. **Mail-in & absentee ballots**: These are counted after Election Day (timing varies by state).\n"
        "3. **Provisional ballots**: Counted after officials verify voter eligibility.\n"
        "4. **Canvassing**: Election boards officially review and confirm the count.\n"
        "5. **Certification**: State officials certify the official results, typically within weeks of Election Day.\n"
        "6. **Recounts**: Automatically triggered in very close races; candidates can also request them.\n\n"
        "Would you like to know more about any specific part of this process?"
    ),
    "mail_in": (
        "**Mail-In & Absentee Voting**\n\n"
        "Mail-in voting allows you to cast your ballot without going to a polling place:\n\n"
        "1. **Request a ballot**: Apply for an absentee or mail-in ballot through your state's election office.\n"
        "2. **Receive your ballot**: It will be mailed to your registered address.\n"
        "3. **Complete the ballot**: Follow all instructions carefully — sign the envelope if required.\n"
        "4. **Return it on time**: Mail it back well before Election Day, or drop it at an official drop box.\n"
        "5. **Track your ballot**: Many states allow you to track your mail-in ballot online.\n\n"
        "Rules vary significantly by state. Visit your state's official election website for exact procedures."
    ),
    "voter_id": (
        "**Voter ID Requirements**\n\n"
        "ID requirements vary by state:\n\n"
        "- **Strict photo ID states**: Must show a government-issued photo ID (driver's license, passport, etc.).\n"
        "- **Non-strict photo ID states**: Photo ID preferred, but alternatives accepted (utility bill, bank statement).\n"
        "- **No ID required states**: Simply state your name and address at the polling place.\n\n"
        "**Tip**: Always check your specific state's requirements at your state's official election website before Election Day to be fully prepared.\n\n"
        "Would you like help finding your state's voter ID requirements?"
    ),
    "inauguration": (
        "**Presidential Inauguration**\n\n"
        "The Inauguration is the ceremony that officially begins a President's term:\n\n"
        "1. **Date**: January 20th (or 21st if January 20th falls on a Sunday) following the election year.\n"
        "2. **Location**: The West Front of the US Capitol Building in Washington, D.C.\n"
        "3. **The Oath**: The President-elect takes the Constitutional oath of office, administered by the Chief Justice of the Supreme Court.\n"
        "4. **Inaugural Address**: The new President delivers their first speech to the nation.\n"
        "5. **Transfer of power**: Power officially transfers from the outgoing to the incoming President at noon on January 20th.\n\n"
        "Is there anything else about the inauguration or the transition process you'd like to know?"
    ),
    "welcome": (
        "🗳️ Welcome to ElectionGuide AI!\n"
        "─────────────────────────────\n"
        "Hi there! 👋 I'm your friendly, step-by-step guide to understanding elections — fully neutral and always clear.\n\n"
        "I can walk you through:\n"
        "- 📋 Voter registration\n"
        "- 🗳️ Primary & general elections\n"
        "- 🗺️ The Electoral College\n"
        "- 📬 Mail-in & absentee voting\n"
        "- 📊 Vote counting & certification\n\n"
        "💬 **To get started:** What election are you curious about?\n"
        "Federal (Presidential/Congressional), State, Local, or a specific upcoming date?"
    ),
    "default": (
        "🗳️ Great Question!\n"
        "─────────────────\n"
        "I'm currently in **demo mode** (no Gemini API key set), but I can still help with key topics!\n\n"
        "📍 Step 1 of 1: Add your API key\n"
        "Open the `.env` file and set `GEMINI_API_KEY=your_key_here` to unlock full AI responses.\n\n"
        "✅ Your Next Steps:\n"
        "1. Get a free key → https://aistudio.google.com/app/apikey\n"
        "2. Paste it in `.env` and restart the server\n\n"
        "🔗 In the meantime, try asking me about:\n"
        "- Voter registration deadlines\n"
        "- The Electoral College\n"
        "- Primary vs. general elections\n"
        "- Mail-in voting rules\n\n"
        "💬 Which state or election type are you most interested in?"
    ),
}
