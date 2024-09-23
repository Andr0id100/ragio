#!/bin/bash

VIDEO_URL="https://f1tv.formula1.com/detail/1000003947/2021-british-grand-prix?action=play"

# Output directory
OUTPUT_DIR="data/video"
AUDIO_DIR="data/audio"

mkdir -p "$AUDIO_DIR"

# List of driver identifiers
DRIVERS=("HAM" "BOT" "VER" "PER" "NOR" "RIC" "LEC" "SAI" "VET" "STR" "ALO" "OCO" "GAS" "TSU" "RAI" "GIO" "RUS" "LAT" "MSC" "MAZ")

# Function to extract audio from video
extract_audio() {
    local input_file="$1"
    local output_file="$2"
    ffmpeg -i "$input_file" -map 0:a:0 -c:a pcm_s16le "$output_file"

}

# Iterate over the list of drivers
for driver in "${DRIVERS[@]}"
do
    echo "Downloading video for driver: $driver"
    
    # Run the f1tv-dl command for each driver
    f1tv-dl "$VIDEO_URL" -c "$driver" -s "480x270" --output-directory "$OUTPUT_DIR"
    echo "Download completed for driver: $driver"
     
    # Find the downloaded video file
    video_file=$(find "$OUTPUT_DIR" -name "*-${driver}.mp4" -print -quit)
    echo "$video_file"
    if [ -n "$video_file" ]; then
        echo "Extracting audio from video for driver: $driver"
        
        audio_file="${AUDIO_DIR}/$(basename "${video_file%.*}").wav"
        
        extract_audio "$video_file" "$audio_file"
        
        echo "Audio extraction completed for driver: $driver"
    else
        echo "Video file not found for driver: $driver"
    fi
    
    echo "-----------------------------------"
done

echo "All downloads and audio extractions completed."
