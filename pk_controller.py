import os
import sys
import argparse
import asyncio
from datetime import datetime
from models import get_tester_class, list_registered_models

async def main():
    parser = argparse.ArgumentParser(description="🛡️ Gemini Channels PK Central Controller (Orchestrator)")
    parser.add_argument("--sa-key", required=True, help="Path to GCP Service Account JSON")
    parser.add_argument("--project", required=True, help="GCP Project ID")
    parser.add_argument("--location", default="global", help="GCP Vertex AI Location")
    parser.add_argument("--api-key", required=True, help="Gemini API Key")
    parser.add_argument("--model", required=True, help="Model ID to run PK test on")
    parser.add_argument("--profile", default=None, help="Traffic Stress Profile name (e.g., standard, concurrency_stress, heavy_burst)")
    parser.add_argument("--trials", type=int, default=None, help="Manual override: Number of side-by-side trials")
    parser.add_argument("--delay", type=float, default=None, help="Manual override: Cooldown delay between trials (seconds)")
    parser.add_argument("--prompt", default=None, help="Custom prompt payload override")
    
    args = parser.parse_args()
    
    # 🕵️ Dynamic strategy lookup from models registry
    tester_class = get_tester_class(args.model)
    if not tester_class:
        print(f"❌ Error: Model '{args.model}' is not recognized or registered in the strategy module!")
        print(f"💡 Registered model keys available to test:")
        for m in list_registered_models():
            print(f"   - {m}")
        sys.exit(1)
        
    # 📊 Resolve Traffic Stress Profile (压测用例)
    profiles = tester_class.get_traffic_profiles()
    selected_profile_key = args.profile
    
    # Fallback to standard if no profile is specified
    if not selected_profile_key:
        selected_profile_key = "standard"
        
    if selected_profile_key not in profiles:
        print(f"⚠️ Warning: Profile '{selected_profile_key}' not found for model '{args.model}'. Fallback to 'standard'.")
        selected_profile_key = "standard"
        
    profile_details = profiles[selected_profile_key]
    profile_display_name = f"{profile_details['name']} ({selected_profile_key})"
    
    # Use profile parameters as base
    trials = profile_details["trials"]
    delay = profile_details["delay"]
    
    # Apply command line parameter overrides if explicitly provided
    if args.trials is not None:
        trials = args.trials
        profile_display_name += f" [Overridden trials={args.trials}]"
    if args.delay is not None:
        delay = args.delay
        profile_display_name += f" [Overridden delay={args.delay}s]"
        
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 🏗️ Instantiate selected model strategy object
    tester = tester_class(
        project_id=args.project,
        location=args.location,
        sa_key=args.sa_key,
        api_key=args.api_key,
        timestamp=timestamp
    )
    
    # Resolve prompt payload (use override if provided, else use the model strategy's custom default)
    prompt = args.prompt if args.prompt else tester.get_default_prompt()
    
    print("=========================================================================")
    print("🎮  Gemini Channels PK Duel: ORCHESTRATOR ACTIVE  🎮")
    print("=========================================================================")
    print(f"  - Orchestrator S/W : Strategy Plugin Pattern v2.0")
    print(f"  - Target Project   : {args.project}")
    print(f"  - Target Model Key : {args.model}")
    print(f"  - Strategy Module  : {tester_class.__name__}")
    print(f"  - Traffic Case (用例): {profile_display_name}")
    print(f"  - Case Description : {profile_details['desc']}")
    print(f"  - Total Test Trials: {trials}")
    print(f"  - Delay Interval   : {delay}s")
    print(f"  - Output Directory : {tester.target_dir}")
    print("=========================================================================\n")
    
    # Run campaign
    await tester.execute_pk_campaign(
        prompt=prompt,
        trials=trials,
        delay=delay,
        profile_name=profile_details["name"]
    )

if __name__ == '__main__':
    if sys.platform == 'darwin':
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())
