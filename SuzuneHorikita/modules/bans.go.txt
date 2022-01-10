package plugs

import (
	"fmt"
	"strconv"
	"strings"
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
)

func Detector(bot *gotgbot.Bot, ctx *ext.Context) error {
    if ctx.EffectiveMessage.SenderChat != nil {
            bot.BanChatSenderChat(
                ctx.EffectiveChat.Id,
                ctx.EffectiveMessage.SenderChat.Id,
                &gotgbot.BanChatSenderChatOpts{},
        )
	bot.SendMessage(
                ctx.EffectiveChat.Id,
                fmt.Sprintf("*%v has sent msg via channel and hence I have banned him!", ctx.EffectiveMessage.SenderChat.Id),
                &gotgbot.SendMessageOpts{ParseMode: "markdown"},
        )

    }
    return nil
}


func UnBan(bot *gotgbot.Bot, ctx *ext.Context) error {
	status, er := bot.GetChatMember(ctx.EffectiveChat.Id, ctx.EffectiveUser.Id)
	if er != nil {
		ctx.EffectiveMessage.Reply(
			bot,
			fmt.Sprintf("*ERROR:*\n`%v`", er),
			&gotgbot.SendMessageOpts{ParseMode: "markdown"},
		)
	}
	stats:= status.GetStatus()
	if stats != "creator" || stats != "administrator" {
		ctx.EffectiveMessage.Reply(
			bot,
			"This command can be only used by admins",
			&gotgbot.SendMessageOpts{ParseMode: "markdown"},
		)
	}
	inp_ := strings.ReplaceAll(ctx.EffectiveMessage.Text,  "/unban ", "")
	inp, ero := strconv.ParseInt(inp_, 10, 64)
	if ero != nil {
		ctx.EffectiveMessage.Reply(
			bot,
			fmt.Sprintf("*ERROR:*\n`%v`", ero.Error()),
			&gotgbot.SendMessageOpts{ParseMode: "markdown"},
		)
		return nil
	}
	out, err := bot.UnbanChatSenderChat(
		ctx.EffectiveChat.Id,
		inp,
	)
	if err != nil {
		ctx.EffectiveMessage.Reply(
			bot,
			fmt.Sprintf("*ERROR:*\n`%v`", err.Error()),
			&gotgbot.SendMessageOpts{ParseMode: "markdown"},
		)
		return nil
	}
	ctx.EffectiveMessage.Reply(
		bot,
		fmt.Sprintf("`%v`", out),
		&gotgbot.SendMessageOpts{ParseMode: "markdown"},
	)
	return nil
}
