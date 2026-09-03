#!/bin/bash

# =========================================================================
# 🏆 GCP Vertex AI vs Gemini API (Google AI Studio) Channel PK Duel Launcher
# =========================================================================

# Ensure we are in the correct directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Cache file paths to save user input for repeated usage
CACHE_KEY_FILE=".api_key_cache"
CACHE_SA_FILE=".sa_path_cache"

echo "========================================================================="
echo "🏆  Channel PK Dual Duel Configurer & Orchestrator Launcher"
echo "========================================================================="

# -------------------------------------------------------------------------
# Step 1: Detect/Configure GCP Service Account (SA) Key
# -------------------------------------------------------------------------
SA_KEY=""
PROJECT_ID=""

# Auto-discover service account files in the workspace
echo "🔍 Auto-discovering GCP Service Account candidate files..."
mapfile -t sa_candidates < <(find .. -name "*.json" ! -name "config.json" ! -name "package.json" ! -name "tsconfig.json" ! -name "bower.json" ! -name "composer.json" 2>/dev/null)

if [ ${#sa_candidates[@]} -gt 0 ]; then
    echo "Found the following candidate JSON files:"
    for i in "${!sa_candidates[@]}"; do
        echo "  [$((i+1))] ${sa_candidates[$i]}"
    done
    echo "  [$(( ${#sa_candidates[@]}+1 ))] Manually enter absolute/relative path"
    
    # Check if there is a cached choice
    DEFAULT_CHOICE=1
    if [ -f "$CACHE_SA_FILE" ]; then
        cached_sa=$(cat "$CACHE_SA_FILE")
        for i in "${!sa_candidates[@]}"; do
            if [ "${sa_candidates[$i]}" = "$cached_sa" ]; then
                DEFAULT_CHOICE=$((i+1))
                break
            fi
        done
    fi
    
    read -p "Select GCP Service Account key file [default: $DEFAULT_CHOICE]: " choice
    choice=${choice:-$DEFAULT_CHOICE}
    
    if [ "$choice" -le "${#sa_candidates[@]}" ] && [ "$choice" -gt 0 ]; then
        SA_KEY="${sa_candidates[$((choice-1))]}"
    else
        read -p "Enter path to your GCP SA JSON file: " SA_KEY
    fi
else
    if [ -f "$CACHE_SA_FILE" ]; then
        cached_sa=$(cat "$CACHE_SA_FILE")
        read -p "Enter path to your GCP SA JSON file [default: $cached_sa]: " SA_KEY
        SA_KEY=${SA_KEY:-$cached_sa}
    else
        read -p "Enter path to your GCP SA JSON file: " SA_KEY
    fi
fi

if [ ! -f "$SA_KEY" ]; then
    echo "❌ Error: File not found at path '$SA_KEY'"
    exit 1
fi

PROJECT_ID=$(python3 -c "import json; print(json.load(open('$SA_KEY'))['project_id'])" 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: Failed to extract 'project_id' from JSON file '$SA_KEY'."
    read -p "Please manually input GCP Project ID: " PROJECT_ID
else
    echo "✅ Successfully parsed Project ID: [$PROJECT_ID]"
fi

echo "$SA_KEY" > "$CACHE_SA_FILE"

# -------------------------------------------------------------------------
# Step 2: Detect/Configure Gemini API Key
# -------------------------------------------------------------------------
API_KEY=""
if [ -n "$GEMINI_API_KEY" ]; then
    API_KEY="$GEMINI_API_KEY"
    echo "✅ Using Gemini API Key from environment variable: [GEMINI_API_KEY]"
elif [ -f "$CACHE_KEY_FILE" ]; then
    cached_key=$(cat "$CACHE_KEY_FILE")
    masked_key="${cached_key:0:6}...${cached_key: -6}"
    read -p "Enter Gemini API key [default: $masked_key]: " input_key
    if [ -z "$input_key" ]; then
        API_KEY="$cached_key"
    else
        API_KEY="$input_key"
    fi
else
    read -p "Enter your Gemini API key (Google AI Studio): " API_KEY
fi

if [ -z "$API_KEY" ]; then
    echo "❌ Error: Gemini API Key is required."
    exit 1
fi

echo "$API_KEY" > "$CACHE_KEY_FILE"

# -------------------------------------------------------------------------
# Step 3: Model and Traffic Stress Case Selector
# -------------------------------------------------------------------------
echo "========================================================================="
echo "🎁 Configuration Loaded Successfully! Orchestration Engine online."
echo "========================================================================="
echo "Select model to run PK on:"
echo "  1) Lite Text PK          : gemini-3.1-flash-lite"
echo "  2) Pro Text PK           : gemini-3.1-pro-preview"
echo "  3) Lite Image PK         : gemini-3.1-flash-lite-image"
echo "  4) Pro Image PK          : gemini-3-pro-image"
echo "  5) 3.5 Standard Flash    : gemini-3.5-flash"
echo "  6) Omni Modality Flash   : gemini-omni-flash-preview"
echo "  7) 3.7 Flash             : gemini-3.7-flash"
echo "  8) 3.8 Flash             : gemini-3.8-flash"
echo "  9) Custom Mode           : Enter your own parameters"
echo "========================================================================="
read -p "Select a preset [1-9]: " preset

case $preset in
  1)
    MODEL="gemini-3.1-flash-lite"
    echo ""
    echo "📊 Choose Traffic Stress Case (压测用例) for $MODEL:"
    echo "  1) 标准巡检 (Standard)          - 5 trials, 1.5s delay"
    echo "  2) 中载压力 (Concurrency Stress) - 20 trials, 0.4s delay"
    echo "  3) 极限高频 (Heavy Burst)        - 40 trials, 0.1s delay"
    read -p "Select stress case [1-3, default: 1]: " case_choice
    case_choice=${case_choice:-1}
    case $case_choice in
      2) PROFILE="concurrency_stress" ;;
      3) PROFILE="heavy_burst" ;;
      *) PROFILE="standard" ;;
    esac
    python3 pk_controller.py --sa-key "$SA_KEY" --api-key "$API_KEY" --project "$PROJECT_ID" --model "$MODEL" --profile "$PROFILE"
    ;;
  2)
    MODEL="gemini-3.1-pro-preview"
    echo ""
    echo "📊 Choose Traffic Stress Case (压测用例) for $MODEL:"
    echo "  1) 标准巡检 (Standard)          - 5 trials, 2.0s delay"
    echo "  2) 中载推理 (Reasoning Stress)   - 10 trials, 1.0s delay"
    echo "  3) 极限吞吐 (Extreme Depth)      - 15 trials, 0.6s delay"
    read -p "Select stress case [1-3, default: 1]: " case_choice
    case_choice=${case_choice:-1}
    case $case_choice in
      2) PROFILE="reasoning_stress" ;;
      3) PROFILE="extreme_depth" ;;
      *) PROFILE="standard" ;;
    esac
    python3 pk_controller.py --sa-key "$SA_KEY" --api-key "$API_KEY" --project "$PROJECT_ID" --model "$MODEL" --profile "$PROFILE"
    ;;
  3)
    MODEL="gemini-3.1-flash-lite-image"
    echo ""
    echo "📊 Choose Traffic Stress Case (压测用例) for $MODEL:"
    echo "  1) 标准画质 (Lite Image Standard)   - 3 trials, 3.0s delay"
    echo "  2) 高频图像 (Image Concurrency Stress) - 8 trials, 1.5s delay"
    read -p "Select stress case [1-2, default: 1]: " case_choice
    case_choice=${case_choice:-1}
    case $case_choice in
      2) PROFILE="stress_blast" ;;
      *) PROFILE="standard" ;;
    esac
    python3 pk_controller.py --sa-key "$SA_KEY" --api-key "$API_KEY" --project "$PROJECT_ID" --model "$MODEL" --profile "$PROFILE"
    ;;
  4)
    MODEL="gemini-3-pro-image"
    echo ""
    echo "📊 Choose Traffic Stress Case (压测用例) for $MODEL:"
    echo "  1) 标准画质 (Pro Image Standard)  - 2 trials, 5.0s delay"
    echo "  2) 图像并发 (Pro Image Stress Blast) - 5 trials, 3.0s delay"
    read -p "Select stress case [1-2, default: 1]: " case_choice
    case_choice=${case_choice:-1}
    case $case_choice in
      2) PROFILE="stress_blast" ;;
      *) PROFILE="standard" ;;
    esac
    python3 pk_controller.py --sa-key "$SA_KEY" --api-key "$API_KEY" --project "$PROJECT_ID" --model "$MODEL" --profile "$PROFILE"
    ;;
  5)
    MODEL="gemini-3.5-flash"
    echo ""
    echo "📊 Choose Traffic Stress Case (压测用例) for $MODEL:"
    echo "  1) 标准巡检 (Standard)          - 5 trials, 1.5s delay"
    echo "  2) 高频并发 (Concurrency Stress) - 25 trials, 0.3s delay"
    echo "  3) 极限冲击 (Heavy Burst)        - 50 trials, 0.1s delay"
    read -p "Select stress case [1-3, default: 1]: " case_choice
    case_choice=${case_choice:-1}
    case $case_choice in
      2) PROFILE="concurrency_stress" ;;
      3) PROFILE="heavy_burst" ;;
      *) PROFILE="standard" ;;
    esac
    python3 pk_controller.py --sa-key "$SA_KEY" --api-key "$API_KEY" --project "$PROJECT_ID" --model "$MODEL" --profile "$PROFILE"
    ;;
  6)
    MODEL="gemini-omni-flash-preview"
    echo ""
    echo "📊 Choose Traffic Stress Case (压测用例) for $MODEL:"
    echo "  1) 标准巡检 (Standard)          - 5 trials, 1.5s delay"
    echo "  2) 并发性能 (Concurrency Stress) - 20 trials, 0.4s delay"
    echo "  3) 极限吞吐 (Heavy Burst)        - 40 trials, 0.1s delay"
    read -p "Select stress case [1-3, default: 1]: " case_choice
    case_choice=${case_choice:-1}
    case $case_choice in
      2) PROFILE="concurrency_stress" ;;
      3) PROFILE="heavy_burst" ;;
      *) PROFILE="standard" ;;
    esac
    python3 pk_controller.py --sa-key "$SA_KEY" --api-key "$API_KEY" --project "$PROJECT_ID" --model "$MODEL" --profile "$PROFILE"
    ;;
  7)
    MODEL="gemini-3.7-flash"
    echo ""
    echo "📊 Choose Traffic Stress Case (压测用例) for $MODEL:"
    echo "  1) 标准巡检 (Standard)          - 5 trials, 1.5s delay"
    echo "  2) 高频并发 (Concurrency Stress) - 25 trials, 0.3s delay"
    echo "  3) 极限冲击 (Heavy Burst)        - 50 trials, 0.1s delay"
    read -p "Select stress case [1-3, default: 1]: " case_choice
    case_choice=${case_choice:-1}
    case $case_choice in
      2) PROFILE="concurrency_stress" ;;
      3) PROFILE="heavy_burst" ;;
      *) PROFILE="standard" ;;
    esac
    python3 pk_controller.py --sa-key "$SA_KEY" --api-key "$API_KEY" --project "$PROJECT_ID" --model "$MODEL" --profile "$PROFILE"
    ;;
  8)
    MODEL="gemini-3.8-flash"
    echo ""
    echo "📊 Choose Traffic Stress Case (压测用例) for $MODEL:"
    echo "  1) 标准巡检 (Standard)          - 5 trials, 1.5s delay"
    echo "  2) 高频并发 (Concurrency Stress) - 25 trials, 0.3s delay"
    echo "  3) 极限冲击 (Heavy Burst)        - 50 trials, 0.1s delay"
    read -p "Select stress case [1-3, default: 1]: " case_choice
    case_choice=${case_choice:-1}
    case $case_choice in
      2) PROFILE="concurrency_stress" ;;
      3) PROFILE="heavy_burst" ;;
      *) PROFILE="standard" ;;
    esac
    python3 pk_controller.py --sa-key "$SA_KEY" --api-key "$API_KEY" --project "$PROJECT_ID" --model "$MODEL" --profile "$PROFILE"
    ;;
  9)
    read -p "Enter model name (e.g. gemini-3-pro-image): " custom_model
    read -p "Enter number of trials: " trials
    read -p "Enter delay in seconds: " delay
    python3 pk_controller.py --sa-key "$SA_KEY" --api-key "$API_KEY" --project "$PROJECT_ID" --model "$custom_model" --trials "$trials" --delay "$delay"
    ;;
  *)
    echo "❌ Invalid preset selection. Exiting."
    exit 1
    ;;
esac
