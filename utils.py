def seconds_to_hours_minutes(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{int(hours)}:{int(minutes)}"


def create_formatted_transcripts(df):
    transcripts = ""
    for i in range(len(df)):
        transcripts += f"""
        <transcript>
            <driver>{df.iloc[i].name}</driver>
            <start_time>{seconds_to_hours_minutes(df.iloc[i].start)}</start_time>
            <end_time>{seconds_to_hours_minutes(df.iloc[i].end)}</end_time>
            <text>{df.iloc[i].text}</text>
        </transcript>
        """
    return transcripts
