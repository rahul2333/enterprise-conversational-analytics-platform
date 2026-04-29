import requests
import streamlit as st

API_URL = "http://localhost:8000/query"

st.set_page_config(page_title="Conversational Analytics Demo", layout="wide")
st.title("Conversational Analytics Demo")

question = st.text_input("Ask a question")
execute = st.checkbox("Execute SQL (if valid)", value=False)


def render_response(payload: dict) -> None:
    st.subheader(payload.get("question", "(no question returned)"))

    col1, col2 = st.columns(2)
    col1.metric("Execution Mode", str(payload.get("execution_mode", "unknown")))
    col2.metric("SQL Valid", "✅" if payload.get("is_sql_valid") else "❌")

    warnings = payload.get("warnings", [])
    for warning in warnings:
        st.warning(str(warning))

    with st.expander("Generated SQL", expanded=True):
        st.code(str(payload.get("generated_sql", "")), language="sql")

    st.markdown("### Results")
    results = payload.get("result", [])
    if isinstance(results, list) and results:
        st.dataframe(results, use_container_width=True)
    else:
        mode = payload.get("execution_mode")
        if mode == "dry_run":
            st.info("SQL generated but not executed.")
        elif mode == "blocked":
            st.error("Execution blocked by guardrails.")
        elif mode == "unavailable":
            st.warning("No warehouse executor configured.")
        elif mode == "error":
            st.error("Execution failed. Check warnings above.")
        else:
            st.info("No rows returned.")

    with st.expander("Retrieved Context"):
        st.json(payload.get("retrieved_context", []))

    with st.expander("Raw Response JSON"):
        st.json(payload)


if st.button("Submit"):
    if not question.strip():
        st.warning("Please enter a question before submitting.")
    else:
        try:
            response = requests.post(
                API_URL,
                json={"question": question, "execute": execute},
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                st.error("API returned an unexpected response format.")
            else:
                render_response(payload)
        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to API at http://localhost:8000. "
                "Start it with: uvicorn src.api.main:app --reload"
            )
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
        except requests.exceptions.HTTPError as exc:
            detail = exc.response.text if exc.response is not None else str(exc)
            st.error(f"API request failed: {detail}")
        except ValueError:
            st.error("API did not return valid JSON.")
        except requests.RequestException as exc:
            st.error(f"Unexpected network error: {exc}")
