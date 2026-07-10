
"""
Chat Component for Yapper Studio
Handles chat history, display, streaming, personality greetings, mood detection, blend badges, and compare mode.
"""

import streamlit as st
from core.gemini_client import load_api_key, stream_response_with_personality
from core.mood_detector import detect_mood, get_suggested_personalities
from core.personality_blender import validate_blend
from core.compare_engine import validate_selection, export_comparison, ComparisonResult
from core.favorites_manager import save_favorite, is_favorite
from core.followup_manager import (
    get_followup_actions,
    validate_context,
    execute_followup
)
from personalities.custom_manager import get_personality, is_custom_personality


def init_chat_history() -> None:
    """Initialize chat history and related state in session state if not present."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_personality" not in st.session_state:
        st.session_state.selected_personality = "Professor"
    if "current_personality" not in st.session_state:
        st.session_state.current_personality = st.session_state.selected_personality
    if "personality_greeting_shown" not in st.session_state:
        st.session_state.personality_greeting_shown = False
    if "current_mood" not in st.session_state:
        st.session_state.current_mood = None
    if "mood_confidence" not in st.session_state:
        st.session_state.mood_confidence = None
    if "suggested_personalities" not in st.session_state:
        st.session_state.suggested_personalities = []
    if "primary_personality" not in st.session_state:
        st.session_state.primary_personality = "Professor"
    if "secondary_personality" not in st.session_state:
        st.session_state.secondary_personality = "Best Friend"
    if "blend_ratio" not in st.session_state:
        st.session_state.blend_ratio = 70


def display_personality_greeting() -> None:
    """Display greeting when personality changes (if needed)."""
    if st.session_state.compare_mode:
        return  # No greeting in compare mode
    # Check if personality has changed (for single mode)
    if not st.session_state.blend_mode and st.session_state.selected_personality != st.session_state.current_personality:
        st.session_state.current_personality = st.session_state.selected_personality
        st.session_state.messages = []
        st.session_state.personality_greeting_shown = False
    # Check if blend config changed
    elif st.session_state.blend_mode:
        pass  # Handle blend mode greeting later if needed

    # Show greeting if needed
    if not st.session_state.personality_greeting_shown or not st.session_state.messages:
        if st.session_state.blend_mode:
            # Show blended greeting
            primary = get_personality(st.session_state.primary_personality, st.session_state.custom_personalities)
            secondary = get_personality(st.session_state.secondary_personality, st.session_state.custom_personalities)
            if primary and secondary:
                greeting = f"{primary['emoji']} {primary['greeting']} (with a bit of {secondary['name']}'s style!)"
                with st.chat_message("assistant"):
                    st.markdown(greeting)
                st.session_state.messages.append({"role": "assistant", "content": greeting})
                st.session_state.personality_greeting_shown = True
        else:
            # Single personality greeting
            personality = get_personality(st.session_state.selected_personality, st.session_state.custom_personalities)
            if personality:
                with st.chat_message("assistant"):
                    st.markdown(f"{personality['emoji']} {personality['greeting']}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"{personality['emoji']} {personality['greeting']}"
                })
                st.session_state.personality_greeting_shown = True


def display_chat_history() -> None:
    """Display all messages in the chat history with blend badges and action buttons if needed."""
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            # Show blend badge if assistant and blend mode is on
            personality_name = None
            personality_emoji = None
            if msg["role"] == "assistant":
                if st.session_state.blend_mode:
                    primary = get_personality(st.session_state.primary_personality, st.session_state.custom_personalities)
                    secondary = get_personality(st.session_state.secondary_personality, st.session_state.custom_personalities)
                    if primary and secondary:
                        st.markdown(f"""
<div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 8px;">
    {primary['emoji']} {primary['name']} + {secondary['emoji']} {secondary['name']} 
    ({st.session_state.blend_ratio}/{100 - st.session_state.blend_ratio})
</div>
""", unsafe_allow_html=True)
                        # For blend mode, we'll use primary personality as the main one for saving
                        personality_name = f"{primary['name']} + {secondary['name']}"
                        personality_emoji = primary['emoji']
                else:
                    personality = get_personality(st.session_state.selected_personality, st.session_state.custom_personalities)
                    if personality:
                        personality_name = personality['name']
                        personality_emoji = personality['emoji']
            
            # Show message
            st.markdown(msg["content"])
            
            # Show action buttons for assistant messages
            if msg["role"] == "assistant" and personality_name and personality_emoji:
                # Find question (previous user message)
                question = ""
                if i > 0 and st.session_state.messages[i-1]["role"] == "user":
                    question = st.session_state.messages[i-1]["content"]
                
                # Check if already a favorite
                already_favorite = is_favorite(
                    st.session_state.favorite_replies,
                    personality_name,
                    question,
                    msg["content"]
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(
                        "⭐ Saved" if already_favorite else "⭐ Save",
                        key=f"save_{i}",
                        disabled=already_favorite
                    ):
                        if not already_favorite:
                            updated_favs, status_msg = save_favorite(
                                st.session_state.favorite_replies,
                                personality_name,
                                personality_emoji,
                                question,
                                msg["content"]
                            )
                            st.session_state.favorite_replies = updated_favs
                            st.toast(status_msg, icon="⭐")
                            st.rerun()
                with col2:
                    if st.button(f"📋 Copy", key=f"copy_{i}"):
                        st.write(f"<script>navigator.clipboard.writeText('{msg['content']}')</script>", unsafe_allow_html=True)
                        st.toast("Copied to clipboard!", icon="✅")


def display_mood_suggestions() -> None:
    """Display detected mood and personality suggestions (if any)."""
    if st.session_state.current_mood and st.session_state.current_mood != "Neutral":
        # Mood info container
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"""
<div style="background-color: white; padding: 16px; border-radius: 12px; border: 1px solid #E5E7EB; margin-bottom: 0;">
    <div style="font-weight: 600; margin-bottom: 8px;">
        {st.session_state.current_mood_emoji if hasattr(st.session_state, 'current_mood_emoji') else '😐'} Mood Detected: {st.session_state.current_mood}
    </div>
    <div style="color: #6B7280; font-size: 0.875rem;">
        Confidence: {st.session_state.mood_confidence}
    </div>
</div>
""", unsafe_allow_html=True)
            with col2:
                st.markdown("Suggested Personalities:")
                # Suggestion buttons
                subcols = st.columns(len(st.session_state.suggested_personalities))
                for i, suggestion in enumerate(st.session_state.suggested_personalities):
                    with subcols[i]:
                        if st.button(f"{suggestion['emoji']} {suggestion['name']}", key=f"suggestion_{suggestion['name']}"):
                            if not st.session_state.blend_mode:
                                st.session_state.selected_personality = suggestion['name']
                            else:
                                st.session_state.primary_personality = suggestion['name']


def render_followup_buttons() -> None:
    """Render follow-up buttons (if not in Compare Mode and we have context)."""
    if st.session_state.compare_mode:
        st.info("Follow-up actions are available only during normal conversations.")
        return
    
    if not validate_context(
        st.session_state.last_user_message,
        st.session_state.last_assistant_message
    ):
        return
    
    followup_actions = get_followup_actions()
    st.markdown("### Quick Follow-Ups")
    # Split into rows of 3 columns for responsive layout
    cols_per_row = 3
    for i in range(0, len(followup_actions), cols_per_row):
        row_actions = followup_actions[i:i+cols_per_row]
        cols = st.columns(len(row_actions))
        for j, (icon, name, _) in enumerate(row_actions):
            with cols[j]:
                if st.button(f"{icon} {name}", key=f"followup_{i+j}"):
                    # Execute followup
                    followup_prompt = execute_followup(
                        icon,
                        st.session_state.last_user_message,
                        st.session_state.last_assistant_message
                    )
                    if followup_prompt:
                        st.session_state.last_followup_action = name
                        # Call handle_user_input logic for this prompt
                        handle_user_direct(followup_prompt)


def handle_user_direct(prompt: str) -> None:
    """Handle user input directly (for follow-up actions)."""
    # Detect mood
    mood_result = detect_mood(prompt)
    st.session_state.current_mood = mood_result["mood"]
    st.session_state.current_mood_emoji = mood_result["emoji"]
    st.session_state.mood_confidence = mood_result["confidence"]
    st.session_state.suggested_personalities = get_suggested_personalities(mood_result["mood"])
    
    # Add user message to history
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check API key
    if not load_api_key():
        st.warning(
            "Please set your GEMINI_API_KEY in the .env file. "
            "Copy .env.example to .env and add your key from Google AI Studio."
        )
        return
    
    # Check blend mode validity
    if st.session_state.blend_mode:
        is_valid, error_msg = validate_blend(
            st.session_state.primary_personality,
            st.session_state.secondary_personality
        )
        if not is_valid:
            st.error(error_msg)
            return
    
    # Save last user message
    st.session_state.last_user_message = prompt
    
    # Call Gemini and stream
    try:
        response_container = st.chat_message("assistant").empty()
        primary = None
        secondary = None
        if st.session_state.blend_mode:
            primary = get_personality(st.session_state.primary_personality, st.session_state.custom_personalities)
            secondary = get_personality(st.session_state.secondary_personality, st.session_state.custom_personalities)
            if primary and secondary:
                response_container.markdown(f"""
<div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 8px;">
    {primary['emoji']} {primary['name']} + {secondary['emoji']} {secondary['name']} 
    ({st.session_state.blend_ratio}/{100 - st.session_state.blend_ratio})
</div>
""", unsafe_allow_html=True)
        
        full_response = ""
        if st.session_state.blend_mode:
            personality = st.session_state.primary_personality
        else:
            personality = st.session_state.selected_personality
        
        for chunk in stream_response_with_personality(
            st.session_state.messages,
            personality
        ):
            full_response += chunk
            if st.session_state.blend_mode and primary and secondary:
                response_container.markdown(f"""
<div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 8px;">
    {primary['emoji']} {primary['name']} + {secondary['emoji']} {secondary['name']} 
    ({st.session_state.blend_ratio}/{100 - st.session_state.blend_ratio})
</div>
{full_response}▌
""", unsafe_allow_html=True)
            else:
                response_container.markdown(full_response + "▌")
        
        if st.session_state.blend_mode and primary and secondary:
            response_container.markdown(f"""
<div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 8px;">
    {primary['emoji']} {primary['name']} + {secondary['emoji']} {secondary['name']} 
    ({st.session_state.blend_ratio}/{100 - st.session_state.blend_ratio})
</div>
{full_response}
""", unsafe_allow_html=True)
        else:
            response_container.markdown(full_response)
        
        # Save last assistant message
        st.session_state.last_assistant_message = full_response
        
        # Add assistant message to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
        
        # Add save/copy buttons
        if st.session_state.blend_mode and primary and secondary:
            pers_name = f"{primary['name']} + {secondary['name']}"
            pers_emoji = primary['emoji']
        else:
            pers = get_personality(st.session_state.selected_personality, st.session_state.custom_personalities)
            pers_name = pers['name']
            pers_emoji = pers['emoji']
        
        already_fav = is_favorite(
            st.session_state.favorite_replies,
            pers_name,
            prompt,
            full_response
        )
        fav_col1, fav_col2 = st.columns(2)
        with fav_col1:
            if st.button(
                "⭐ Saved" if already_fav else "⭐ Save",
                key=f"save_followup",
                disabled=already_fav
            ):
                if not already_fav:
                    updated_favs, status_msg = save_favorite(
                        st.session_state.favorite_replies,
                        pers_name,
                        pers_emoji,
                        prompt,
                        full_response
                    )
                    st.session_state.favorite_replies = updated_favs
                    st.toast(status_msg, icon="⭐")
                    st.rerun()
        with fav_col2:
            if st.button("📋 Copy", key=f"copy_followup"):
                st.write(f"<script>navigator.clipboard.writeText('{full_response}')</script>", unsafe_allow_html=True)
                st.toast("Copied to clipboard!", icon="✅")
    except Exception as e:
        st.error(f"Oops! Something went wrong: {str(e)}")


def handle_compare_mode(prompt: str) -> None:
    """Handle user input when in Compare Mode."""
    # Validate selection again
    is_valid, error_msg = validate_selection(st.session_state.compare_personalities)
    if not is_valid:
        st.error(error_msg)
        return

    # Display user prompt
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check API key
    if not load_api_key():
        st.warning(
            "Please set your GEMINI_API_KEY in the .env file. "
            "Copy .env.example to .env and add your key from Google AI Studio."
        )
        return

    # Generate responses for each personality
    results: list[ComparisonResult] = []
    progress_container = st.empty()
    response_containers = {}

    # Initialize progress display
    progress_container.markdown("Generating responses...")

    # Create containers for each personality
    for personality_name in st.session_state.compare_personalities:
        pers = get_personality(personality_name, st.session_state.custom_personalities)
        response_containers[personality_name] = st.container()
        results.append(ComparisonResult(
            personality_name=personality_name,
            personality_emoji=pers["emoji"] if pers else "🤖"
        ))

    # Generate responses one by one
    for idx, personality_name in enumerate(st.session_state.compare_personalities):
        # Update progress
        progress_text = "Generating responses...\n"
        for i, res in enumerate(results):
            if i < idx:
                progress_text += f"- {res.personality_emoji} {res.personality_name} ✓\n"
            elif i == idx:
                progress_text += f"- {res.personality_emoji} {res.personality_name} ...\n"
            else:
                progress_text += f"- {res.personality_emoji} {res.personality_name}\n"
        progress_container.markdown(progress_text.replace("\n", "  \n"))
        
        try:
            # Create a temporary messages list for this personality
            temp_messages = [{"role": "user", "content": prompt}]
            full_response = ""
            pers_data = get_personality(personality_name, st.session_state.custom_personalities)
            with response_containers[personality_name]:
                with st.expander(f"{results[idx].personality_emoji} {personality_name}", expanded=True):
                    resp_placeholder = st.empty()
                    for chunk in stream_response_with_personality(temp_messages, personality_name):
                        full_response += chunk
                        resp_placeholder.markdown(full_response + "▌")
                    resp_placeholder.markdown(full_response)
                    # Action buttons
                    already_favorite = is_favorite(
                        st.session_state.favorite_replies,
                        personality_name,
                        prompt,
                        full_response
                    )
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(
                            "⭐ Saved" if already_favorite else "⭐ Save",
                            key=f"save_{personality_name}_{len(st.session_state.messages)}",
                            disabled=already_favorite
                        ):
                            if not already_favorite:
                                updated_favs, status_msg = save_favorite(
                                    st.session_state.favorite_replies,
                                    personality_name,
                                    pers_data["emoji"] if pers_data else "🤖",
                                    prompt,
                                    full_response
                                )
                                st.session_state.favorite_replies = updated_favs
                                st.toast(status_msg, icon="⭐")
                                st.rerun()
                    with col2:
                        if st.button(f"📋 Copy", key=f"copy_{personality_name}_{len(st.session_state.messages)}"):
                            st.write(f"<script>navigator.clipboard.writeText('{full_response}')</script>", unsafe_allow_html=True)
                            st.toast("Copied to clipboard!", icon="✅")
            results[idx].response = full_response
        except Exception as e:
            results[idx].error = str(e)
            with response_containers[personality_name]:
                with st.expander(f"{results[idx].personality_emoji} {personality_name}", expanded=True):
                    st.error(f"Error: {str(e)}")

    # Clear progress container
    progress_container.empty()

    # Add to session state
    st.session_state.last_comparison = {
        "question": prompt,
        "results": results
    }

    # Add export button
    if st.session_state.last_comparison:
        export_md = export_comparison(
            st.session_state.last_comparison["question"],
            st.session_state.last_comparison["results"]
        )
        st.download_button(
            label="📥 Export Comparison",
            data=export_md,
            file_name="comparison.md",
            mime="text/markdown"
        )


def handle_user_input() -> None:
    """
    Handle user input: detect mood, append to history, display, call Gemini, stream response.
    """
    if prompt := st.chat_input("Ask anything..."):
        if st.session_state.compare_mode:
            handle_compare_mode(prompt)
            return
        # Detect mood
        mood_result = detect_mood(prompt)
        st.session_state.current_mood = mood_result["mood"]
        st.session_state.current_mood_emoji = mood_result["emoji"]
        st.session_state.mood_confidence = mood_result["confidence"]
        st.session_state.suggested_personalities = get_suggested_personalities(mood_result["mood"])
        
        # Add and display user message
        user_msg = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Check if API key is present
        if not load_api_key():
            st.warning(
                "Please set your GEMINI_API_KEY in the .env file. "
                "Copy .env.example to .env and add your key from Google AI Studio."
            )
            return
        
        # Check blend mode validity
        if st.session_state.blend_mode:
            is_valid, error_msg = validate_blend(
                st.session_state.primary_personality,
                st.session_state.secondary_personality
            )
            if not is_valid:
                st.error(error_msg)
                return
        
        # Save last user message
        st.session_state.last_user_message = prompt

        # Call Gemini and stream response
        try:
            response_container = st.chat_message("assistant").empty()
            primary = None
            secondary = None
            # Show blend badge in response container
            if st.session_state.blend_mode:
                primary = get_personality(st.session_state.primary_personality, st.session_state.custom_personalities)
                secondary = get_personality(st.session_state.secondary_personality, st.session_state.custom_personalities)
                if primary and secondary:
                    response_container.markdown(f"""
<div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 8px;">
    {primary['emoji']} {primary['name']} + {secondary['emoji']} {secondary['name']} 
    ({st.session_state.blend_ratio}/{100 - st.session_state.blend_ratio})
</div>
""", unsafe_allow_html=True)
            
            full_response = ""
            # Determine personality to use
            if st.session_state.blend_mode:
                personality = st.session_state.primary_personality  # Pass primary, blend inside gemini client
            else:
                personality = st.session_state.selected_personality
            
            for chunk in stream_response_with_personality(
                st.session_state.messages,
                personality
            ):
                full_response += chunk
                # Re-render badge + response
                if st.session_state.blend_mode and primary and secondary:
                    response_container.markdown(f"""
<div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 8px;">
    {primary['emoji']} {primary['name']} + {secondary['emoji']} {secondary['name']} 
    ({st.session_state.blend_ratio}/{100 - st.session_state.blend_ratio})
</div>
{full_response}▌
""", unsafe_allow_html=True)
                else:
                    response_container.markdown(full_response + "▌")
            
            # Final render without cursor
            if st.session_state.blend_mode and primary and secondary:
                response_container.markdown(f"""
<div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 8px;">
    {primary['emoji']} {primary['name']} + {secondary['emoji']} {secondary['name']} 
    ({st.session_state.blend_ratio}/{100 - st.session_state.blend_ratio})
</div>
{full_response}
""", unsafe_allow_html=True)
            else:
                response_container.markdown(full_response)
            
            # Save last assistant message
            st.session_state.last_assistant_message = full_response
            
            # Add action buttons below final response
            if st.session_state.blend_mode and primary and secondary:
                personality_name = f"{primary['name']} + {secondary['name']}"
                personality_emoji = primary['emoji']
            else:
                pers = get_personality(st.session_state.selected_personality, st.session_state.custom_personalities)
                personality_name = pers['name']
                personality_emoji = pers['emoji']
            
            already_favorite = is_favorite(
                st.session_state.favorite_replies,
                personality_name,
                prompt,
                full_response
            )
            button_col1, button_col2 = st.columns(2)
            with button_col1:
                if st.button(
                    "⭐ Saved" if already_favorite else "⭐ Save",
                    key="save_current",
                    disabled=already_favorite
                ):
                    if not already_favorite:
                        updated_favs, status_msg = save_favorite(
                            st.session_state.favorite_replies,
                            personality_name,
                            personality_emoji,
                            prompt,
                            full_response
                        )
                        st.session_state.favorite_replies = updated_favs
                        st.toast(status_msg, icon="⭐")
                        st.rerun()
            with button_col2:
                if st.button(f"📋 Copy", key="copy_current"):
                    st.write(f"<script>navigator.clipboard.writeText('{full_response}')</script>", unsafe_allow_html=True)
                    st.toast("Copied to clipboard!", icon="✅")

            # Save assistant message
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)}")


def render_chat() -> None:
    """Render the complete chat interface."""
    init_chat_history()
    if not st.session_state.compare_mode:
        display_personality_greeting()
        display_chat_history()
        display_mood_suggestions()
        render_followup_buttons()
    else:
        # Display last comparison if exists
        if st.session_state.last_comparison:
            question = st.session_state.last_comparison["question"]
            with st.chat_message("user"):
                st.markdown(question)
            for res in st.session_state.last_comparison["results"]:
                with st.expander(f"{res.personality_emoji} {res.personality_name}", expanded=True):
                    if res.error:
                        st.error(f"Error: {res.error}")
                    else:
                        st.markdown(res.response)
                    
                    # Action buttons
                    if res.response:
                        already_favorite = is_favorite(
                            st.session_state.favorite_replies,
                            res.personality_name,
                            question,
                            res.response
                        )
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(
                                "⭐ Saved" if already_favorite else "⭐ Save",
                                key=f"save_{res.personality_name}_last",
                                disabled=already_favorite
                            ):
                                if not already_favorite:
                                    updated_favs, status_msg = save_favorite(
                                        st.session_state.favorite_replies,
                                        res.personality_name,
                                        res.personality_emoji,
                                        question,
                                        res.response
                                    )
                                    st.session_state.favorite_replies = updated_favs
                                    st.toast(status_msg, icon="⭐")
                                    st.rerun()
                        with col2:
                            if st.button(f"📋 Copy", key=f"copy_{res.personality_name}_last"):
                                st.write(f"<script>navigator.clipboard.writeText('{res.response}')</script>", unsafe_allow_html=True)
                                st.toast("Copied to clipboard!", icon="✅")
            # Export button
            export_md = export_comparison(
                st.session_state.last_comparison["question"],
                st.session_state.last_comparison["results"]
            )
            st.download_button(
                label="📥 Export Comparison",
                data=export_md,
                file_name="comparison.md",
                mime="text/markdown"
            )
    handle_user_input()

