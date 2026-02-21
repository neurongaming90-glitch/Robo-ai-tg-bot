import os
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, InlineQueryHandler, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
import uuid

from ai_engine import AIEngine
from wiki_engine import WikiEngine

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize engines
ai_engine = AIEngine()
wiki_engine = WikiEngine()

# User modes storage (in-memory)
user_modes = {}

# Mode configurations
MODES = {
    'smart': {
        'name': '🧠 Smart Mode',
        'description': 'Intelligent and accurate responses',
        'system_prompt': 'You are an intelligent AI assistant. Provide accurate, helpful, and detailed responses.'
    },
    'funny': {
        'name': '😂 Funny Mode',
        'description': 'Humorous and entertaining responses',
        'system_prompt': 'You are a funny and witty AI comedian. Make responses entertaining and humorous while still being helpful.'
    },
    'savage': {
        'name': '🔥 Savage Mode',
        'description': 'Direct and no-nonsense responses',
        'system_prompt': 'You are a savage AI that gives direct, no-nonsense, brutally honest responses. Be witty and sarcastic.'
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user_id = update.effective_user.id
    
    # Set default mode if not set
    if user_id not in user_modes:
        user_modes[user_id] = 'smart'
    
    welcome_text = (
        "🤖 <b>AI Inline Bot</b>\n\n"
        "Use me inline by typing: <code>@" + context.bot.username + " your question</code>\n\n"
        "Commands:\n"
        "• /mode - Switch personality mode\n"
        "• /help - Get help\n\n"
        f"Current mode: {MODES[user_modes[user_id]]['name']}"
    )
    
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.HTML)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = (
        "📚 <b>Help & Features</b>\n\n"
        "<b>Inline Queries:</b>\n"
        "Type: @botname your question\n"
        "Get AI-powered responses based on your current mode\n\n"
        "<b>Personality Modes:</b>\n"
        f"🧠 {MODES['smart']['description']}\n"
        f"😂 {MODES['funny']['description']}\n"
        f"🔥 {MODES['savage']['description']}\n\n"
        "<b>Features:</b>\n"
        "• AI-powered responses using DeepSeek\n"
        "• Wikipedia integration for factual queries\n"
        "• Multiple personality modes\n"
        "• Fast and accurate inline responses"
    )
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

async def mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /mode command"""
    user_id = update.effective_user.id
    
    if user_id not in user_modes:
        user_modes[user_id] = 'smart'
    
    current_mode = user_modes[user_id]
    
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = [[InlineKeyboardButton(
        text=f"✓ {MODES[mode_key]['name']}" if mode_key == current_mode else MODES[mode_key]['name'],
        callback_data=f'mode_{mode_key}'
    ) for mode_key in MODES.keys()]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    mode_text = f"Current mode: {MODES[current_mode]['name']}\n\nSelect new mode:"
    await update.message.reply_text(mode_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if query.data.startswith('mode_'):
        new_mode = query.data.split('_')[1]
        user_modes[user_id] = new_mode
        
        await query.answer(f"✓ Switched to {MODES[new_mode]['name']}", show_alert=False)
        await query.edit_message_text(
            text=f"✓ Mode switched to {MODES[new_mode]['name']}",
            parse_mode=ParseMode.HTML
        )

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline queries"""
    query_text = update.inline_query.query
    user_id = update.inline_query.from_user.id
    
    if not query_text:
        return
    
    # Get user's current mode
    current_mode = user_modes.get(user_id, 'smart')
    mode_prompt = MODES[current_mode]['system_prompt']
    
    try:
        # Try to fetch Wikipedia summary for factual queries
        wiki_summary = None
        try:
            wiki_summary = wiki_engine.get_summary(query_text)
        except Exception as e:
            logger.info(f"Wikipedia fetch skipped: {e}")
        
        # Get AI response
        ai_response = await ai_engine.generate_response(
            query=query_text,
            system_prompt=mode_prompt,
            wiki_context=wiki_summary
        )
        
        # Format response
        title = f"{MODES[current_mode]['name']} Response"
        description = ai_response[:100] + "..." if len(ai_response) > 100 else ai_response
        
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=title,
                description=description,
                input_message_content=InputTextMessageContent(
                    message_text=ai_response,
                    parse_mode=ParseMode.HTML
                ),
                thumb_url="https://via.placeholder.com/48"
            )
        ]
        
        await update.inline_query.answer(results, cache_time=10)
        
    except Exception as e:
        logger.error(f"Error processing inline query: {e}")
        
        # Fallback response
        fallback_response = f"Sorry, I encountered an error processing your query. Please try again later."
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="❌ Error",
                description="Failed to process request",
                input_message_content=InputTextMessageContent(
                    message_text=fallback_response,
                    parse_mode=ParseMode.HTML
                )
            )
        ]
        await update.inline_query.answer(results)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Exception while handling an update: {context.error}")

def main() -> None:
    """Main function to start the bot"""
    # Bot token hardcoded (for deployment)
    bot_token = "8466855802:AAEvmgoVf7D-AVa9h_x4gpL8P6Cakhgzzzk"
    
    if not bot_token:
        raise ValueError("BOT_TOKEN environment variable not set")
    
    # Create application
    application = Application.builder().token(bot_token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mode", mode_command))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    logger.info("Bot started. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()