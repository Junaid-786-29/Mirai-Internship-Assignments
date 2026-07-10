
"""
Sidebar Component for Yapper Studio - Clean, Minimal Design
"""

import streamlit as st
from personalities.custom_manager import (
    get_all_personality_names,
    get_personality,
    is_custom_personality,
    create_personality,
    update_personality,
    export_personality_to_json,
    import_personality_from_json
)
from core.personality_blender import validate_blend, get_blend_summary
from core.compare_engine import validate_selection
from core.favorites_manager import (
    search_favorites,
    sort_favorites,
    delete_favorite,
    export_favorites
)
from dataclasses import asdict


def render_sidebar() -> None:
    """Render the sidebar with personality, settings, etc."""
    with st.sidebar:
        # Logo & Title
        st.markdown("# 🤖 Yapper Studio")
        st.caption("One AI. Infinite Personalities.")
        st.divider()

        # New Chat Button
        if st.button("➕ New Chat", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.personality_greeting_shown = False
            st.session_state.last_comparison = None
        st.divider()

        # Handle mutual exclusivity between Blend & Compare Mode
        if st.session_state.compare_mode and st.session_state.blend_mode:
            # Determine which one was just toggled - use the one that's True, set other to False
            # Check if we were previously in compare mode
            if st.session_state.get("last_mode") == "compare":
                st.session_state.blend_mode = False
            else:
                st.session_state.compare_mode = False
            st.info("Blend Mode and Compare Mode cannot be used at the same time!")
        # Track last mode for mutual exclusivity
        if st.session_state.compare_mode:
            st.session_state.last_mode = "compare"
        elif st.session_state.blend_mode:
            st.session_state.last_mode = "blend"

        # Compare Mode Checkbox
        st.checkbox("📊 Compare Mode", key="compare_mode")
        if not st.session_state.compare_mode:
            # Blend Mode Checkbox (only if compare is off)
            st.checkbox("⚖️ Blend Mode", key="blend_mode")
        st.divider()

        # Personality Selector
        all_personalities = get_all_personality_names(st.session_state.custom_personalities)
        if st.session_state.compare_mode:
            # Compare mode: multi-select personalities
            st.markdown("### 🎭 Select Personalities to Compare")
            st.multiselect(
                "Select Personalities to Compare",
                all_personalities,
                key="compare_personalities",
                label_visibility="collapsed",
                default=st.session_state.compare_personalities
            )
            # Validate selection
            is_valid, error_msg = validate_selection(st.session_state.compare_personalities)
            if not is_valid:
                st.warning(error_msg)
        elif not st.session_state.blend_mode:
            # Single personality
            st.markdown("### 🎭 Personality")
            st.selectbox(
                "Select Personality",
                all_personalities,
                key="selected_personality",
                label_visibility="collapsed"
            )
        else:
            # Blended personalities
            st.markdown("### 🎭 Blended Personalities")
            
            # Primary
            st.selectbox(
                "Primary Personality",
                all_personalities,
                key="primary_personality",
                index=0
            )
            
            # Secondary
            secondary_index = 1 if (st.session_state.primary_personality == all_personalities[0]) else 0
            st.selectbox(
                "Secondary Personality",
                all_personalities,
                key="secondary_personality",
                index=secondary_index
            )
            
            # Blend Ratio Slider
            st.slider(
                "Blend Ratio (Primary %)",
                min_value=0,
                max_value=100,
                value=70,
                step=1,
                key="blend_ratio"
            )
            
            # Validate blend
            is_valid, error_msg = validate_blend(
                st.session_state.primary_personality,
                st.session_state.secondary_personality
            )
            if not is_valid:
                st.warning(error_msg)
            else:
                # Show blend summary
                summary = get_blend_summary(
                    st.session_state.primary_personality,
                    st.session_state.secondary_personality,
                    st.session_state.blend_ratio
                )
                st.caption(summary)
        
        st.divider()

        # Creativity Slider
        st.markdown("### 🎨 Creativity")
        st.slider(
            "Creativity",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            key="temperature",
            label_visibility="collapsed"
        )
        st.divider()

        # Favorite Replies
        st.markdown("### ⭐ Favorite Replies")
        if st.session_state.favorite_replies:
            # Search box
            search_query = st.text_input("Search Favorites", placeholder="Search by question, response, or personality...", key="favorites_search")
            
            # Sort dropdown
            sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Personality Name"], key="favorites_sort")
            sort_map = {
                "Newest First": "newest",
                "Oldest First": "oldest",
                "Personality Name": "personality"
            }
            
            # Get filtered and sorted favorites
            filtered = search_favorites(st.session_state.favorite_replies, search_query)
            sorted_favs = sort_favorites(filtered, sort_map[sort_by])
            
            # Display favorites
            for fav in sorted_favs:
                with st.expander(f"{fav['emoji']} {fav['personality']}"):
                    st.markdown(f"**Question:**")
                    st.markdown(fav['question'])
                    st.markdown("**Response:**")
                    st.markdown(fav['response'])
                    st.markdown(f"**Saved at:** {fav['timestamp']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"📋 Copy", key=f"copy_fav_{fav['id']}"):
                            st.write(f"<script>navigator.clipboard.writeText('{fav['response']}')</script>", unsafe_allow_html=True)
                            st.toast("Copied to clipboard!", icon="✅")
                    with col2:
                        if st.button(f"🗑 Delete", key=f"delete_fav_{fav['id']}"):
                            if f"confirm_delete_{fav['id']}" not in st.session_state:
                                st.session_state[f"confirm_delete_{fav['id']}"] = False
                            if not st.session_state[f"confirm_delete_{fav['id']}"]:
                                st.warning("Click again to confirm deletion.")
                                st.session_state[f"confirm_delete_{fav['id']}"] = True
                            else:
                                st.session_state.favorite_replies = delete_favorite(st.session_state.favorite_replies, fav['id'])
                                st.toast("Favorite deleted!", icon="🗑️")
                                st.rerun()
            
            # Export button
            export_md = export_favorites(st.session_state.favorite_replies)
            st.download_button(
                "📥 Export Favorites",
                data=export_md,
                file_name="favorites.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.caption("No favorite replies yet.")
        st.divider()

        # --------------------------
        # Custom Personality Manager
        # --------------------------
        with st.expander("➕ Create/Edit Personality", expanded=False):
            # Initialize form mode state
            if "edit_mode" not in st.session_state:
                st.session_state.edit_mode = False
            if "editing_personality_name" not in st.session_state:
                st.session_state.editing_personality_name = None

            # Get existing custom personality names for dropdown
            custom_personality_names = list(st.session_state.custom_personalities.keys())
            if custom_personality_names:
                edit_selection = st.selectbox(
                    "Edit existing (or leave blank for new)",
                    ["--- Create New ---"] + custom_personality_names
                )
                if edit_selection != "--- Create New ---":
                    st.session_state.edit_mode = True
                    st.session_state.editing_personality_name = edit_selection
                else:
                    st.session_state.edit_mode = False
                    st.session_state.editing_personality_name = None
            else:
                st.session_state.edit_mode = False
                st.session_state.editing_personality_name = None

            # Get default values for form
            if st.session_state.edit_mode and st.session_state.editing_personality_name:
                default_personality = st.session_state.custom_personalities[st.session_state.editing_personality_name]
                default_name = default_personality["name"]
                default_desc = default_personality["description"]
                default_role = default_personality["role"]
                default_tone = default_personality["tone"]
                default_speaking = default_personality["speaking_style"]
                default_knowledge = default_personality["knowledge_area"]
                default_humor = default_personality["humor_level"]
                default_greeting = default_personality["greeting"]
                default_catchphrase = default_personality["catchphrase"]
                default_instructions = default_personality["special_instructions"]
            else:
                default_name = ""
                default_desc = ""
                default_role = ""
                default_tone = "Friendly"
                default_speaking = "Conversational"
                default_knowledge = ""
                default_humor = 5
                default_greeting = "Hello! How can I help you today?"
                default_catchphrase = ""
                default_instructions = ""

            # Create form
            with st.form("personality_form", clear_on_submit=False):
                st.markdown("#### Personality Details")
                name = st.text_input("Name *", value=default_name)
                description = st.text_area("Description", value=default_desc)
                role = st.text_input("Role *", value=default_role)
                
                col1, col2 = st.columns(2)
                with col1:
                    tone = st.selectbox(
                        "Tone",
                        ["Friendly", "Professional", "Funny", "Formal", "Energetic", "Calm"],
                        index=["Friendly", "Professional", "Funny", "Formal", "Energetic", "Calm"].index(default_tone)
                    )
                with col2:
                    speaking_style = st.selectbox(
                        "Speaking Style",
                        ["Simple", "Detailed", "Technical", "Storytelling", "Conversational"],
                        index=["Simple", "Detailed", "Technical", "Storytelling", "Conversational"].index(default_speaking)
                    )
                
                knowledge_area = st.text_input("Knowledge Area (e.g., Python, Java, AI)", value=default_knowledge)
                humor_level = st.slider("Humor Level (0-10)", 0, 10, value=default_humor)
                greeting = st.text_input("Greeting Message", value=default_greeting)
                catchphrase = st.text_input("Catchphrase", value=default_catchphrase)
                special_instructions = st.text_area("Special Instructions", value=default_instructions)

                # Submit button
                submitted = st.form_submit_button(
                    "Update Personality" if st.session_state.edit_mode else "Create Personality",
                    use_container_width=True
                )

                if submitted:
                    # Get all existing names (predefined + custom)
                    all_names = get_all_personality_names(st.session_state.custom_personalities)
                    if st.session_state.edit_mode:
                        # Exclude the current name being edited from duplicates check
                        existing_names_for_validation = [n for n in all_names if n != st.session_state.editing_personality_name]
                        updated_personality, error = update_personality(
                            st.session_state.editing_personality_name,
                            name,
                            description,
                            role,
                            tone,
                            speaking_style,
                            knowledge_area,
                            humor_level,
                            catchphrase,
                            greeting,
                            special_instructions,
                            existing_names_for_validation
                        )
                        if error:
                            st.error(error)
                        else:
                            # Update session state
                            st.session_state.custom_personalities[name] = asdict(updated_personality)
                            if name != st.session_state.editing_personality_name:
                                # Remove old name if changed
                                del st.session_state.custom_personalities[st.session_state.editing_personality_name]
                                # Update selected personality if it was the old one
                                if st.session_state.selected_personality == st.session_state.editing_personality_name:
                                    st.session_state.selected_personality = name
                            st.success(f"Updated personality: {name}")
                            st.session_state.edit_mode = False
                            st.session_state.editing_personality_name = None
                            st.rerun()
                    else:
                        # Create new personality
                        new_personality, error = create_personality(
                            name,
                            description,
                            role,
                            tone,
                            speaking_style,
                            knowledge_area,
                            humor_level,
                            catchphrase,
                            greeting,
                            special_instructions,
                            all_names
                        )
                        if error:
                            st.error(error)
                        else:
                            # Save to session state
                            st.session_state.custom_personalities[name] = asdict(new_personality)
                            st.success(f"Created personality: {name}")
                            st.rerun()

        # Delete/Export buttons for custom personalities
        if custom_personality_names:
            st.markdown("#### Custom Personality Tools")
            selected_custom = st.selectbox(
                "Select custom personality to manage",
                custom_personality_names
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🗑️ Delete {selected_custom}", use_container_width=True):
                    if "confirm_delete" not in st.session_state:
                        st.session_state.confirm_delete = False
                    if not st.session_state.confirm_delete:
                        st.warning(f"Are you sure you want to delete {selected_custom}? Click again to confirm.")
                        st.session_state.confirm_delete = True
                    else:
                        del st.session_state.custom_personalities[selected_custom]
                        # If deleted personality was selected, reset to first personality
                        if st.session_state.selected_personality == selected_custom:
                            all_pers = get_all_personality_names(st.session_state.custom_personalities)
                            if all_pers:
                                st.session_state.selected_personality = all_pers[0]
                        st.success(f"Deleted personality: {selected_custom}")
                        st.session_state.confirm_delete = False
                        st.rerun()
            with col2:
                # Export
                personality_to_export = st.session_state.custom_personalities[selected_custom]
                json_str = export_personality_to_json(personality_to_export)
                st.download_button(
                    label=f"📥 Export {selected_custom}",
                    data=json_str,
                    file_name=f"{selected_custom.replace(' ', '_')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            st.divider()

        # Import
        st.markdown("#### Import Personality")
        uploaded_file = st.file_uploader("Upload JSON file", type="json")
        if uploaded_file is not None:
            try:
                json_str = uploaded_file.getvalue().decode("utf-8")
                all_names = get_all_personality_names(st.session_state.custom_personalities)
                imported_personality, error = import_personality_from_json(json_str, all_names)
                if error:
                    st.error(error)
                else:
                    st.session_state.custom_personalities[imported_personality.name] = asdict(imported_personality)
                    st.success(f"Imported personality: {imported_personality.name}")
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to import: {str(e)}")

