from skills.cultural_interviewer_skill import (
    tribal_interviewer,
    agrarian_interviewer,
    maritime_interviewer,
    build_cultural_interviewer_skill,
    InterviewConfig,
)

print("=== Cultural Interviewer Skills ===")
print(f"Tribal  : {tribal_interviewer.name}")
print(f"Agrarian: {agrarian_interviewer.name}")
print(f"Maritime: {maritime_interviewer.name}")

# Build a custom skill
custom = build_cultural_interviewer_skill(
    InterviewConfig(
        community_context="urban",
        primary_language="en",
        session_duration_mins=30,
        sensitive_topics_excluded=["religion"],
    )
)
print(f"Custom  : {custom.name}")
print("\n✅ All 4 Cultural Interviewer Skills instantiated successfully")
print("✅ Exportable via: adk skill export cultural_interviewer")
