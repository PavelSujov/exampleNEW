# Project Architecture Rules (Non-Obvious Only)

## System Design
- Modular architecture with strict separation: data_loader, analysis, plotting, decrypting modules
- Each module must remain under 400 lines as per project constraints
- Caching strategy uses @st.cache_data decorator for performance optimization

## Data Flow Architecture
- Data flows from Excel files → data_loader → analysis → plotting pipeline
- All operations must preserve Russian column names throughout the pipeline
- User-uploaded databases must follow the same structure as the default database