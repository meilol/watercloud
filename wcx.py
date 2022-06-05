#Watercloud menu system
import asyncio

class Menu:
    class Submenu:
        def __init__(self, name, content):
            self.content = content
            self.leadsTo = []
            self.name = name
            
        def getText(self):
            text = ""
            for idx, menu in enumerate(self.leadsTo):
                text += "[{}] {}\n".format(idx+1, menu.name)
            return text
                
        def getChild(self, childIndex):
            try:
                return self.leadsTo[childIndex]
            except IndexError:
                raise IndexError("child index out of range")
                
        def addChild(self, child):
            self.leadsTo.append(child)
            
    class InputSubmenu:
        """A metaclass of the Menu class for submenu options that take input, instead of prompting the user to pick an option."""
        def __init__(self, name, content, inputFunction, leadsTo):
            self.content = content
            self.name = name
            self.inputFunction = inputFunction
            self.leadsTo = leadsTo
            
        def nextChild(self):
            return self.leadsTo
            
    class ChoiceSubmenu:
        """A metaclass of the Menu class for submenu options for choosing an option from a list."""
        def __init__(self, name, content, options, inputFunction, leadsTo):
            self.content = content
            self.name = name
            self.options = options
            self.inputFunction = inputFunction
            self.leadsTo = leadsTo
            
        def nextChild(self):
            return self.leadsTo
            
    
    def __init__(self, mainPage):
        self.children = []
        self.main = self.Submenu("main", mainPage)
        
    def addChild(self, child):
        self.main.addChild(child)
        
    async def start(self, ctx):
        current = self.main
        menuMsg = None
        while True:
            output = ""       
        
            if type(current) == self.Submenu:
                if type(current.content) == str:
                    output += current.content + "\n"
                elif callable(current.content):
                    current.content()
                else:
                    raise TypeError("submenu body is not a str or function")
                    
                if not current.leadsTo:
                    if not menuMsg:
                        menuMsg = await ctx.send("```" + output + "```")
                    else:
                        await menuMsg.edit(content="```" + output + "```")
                    break
                    
                output += "\n" + current.getText() + "\n"
                output += "Enter a number."
                
                if not menuMsg:
                    menuMsg = await ctx.send("```" + output + "```")
                else:
                    await menuMsg.edit(content="```" + output + "```")
                    
                reply = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.bot.user and m.content.isdigit() and m.channel == ctx.message.channel)
                await reply.delete()
                
                try:
                    current = current.getChild(int(reply.content) - 1)
                except IndexError:
                    print("Invalid number.")
                    break
                    
            elif type(current) == self.InputSubmenu:
                if type(current.content) == list:
                    answers = []
                    for question in current.content:
                        await menuMsg.edit(content="```" + question + "\n\nEnter a value." + "```")
                        reply = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.bot.user and m.channel == ctx.message.channel)
                        await reply.delete()
                        answers.append(reply)
                    current.inputFunction(*answers)
                else:
                    await menuMsg.edit(content="```" + current.content + "\n\nEnter a value." + "```")
                    reply = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.bot.user and m.channel == ctx.message.channel)
                    await reply.delete()
                    current.inputFunction(reply)
                
                if not current.leadsTo:
                    break
                    
                current = current.leadsTo
            
            elif type(current) == self.ChoiceSubmenu:
                result = "```" + current.content + "\n\n"
                if type(current.options) == dict:
                    indexes = {}
                    for idx, option in enumerate(current.options):
                        result += "[{}] {}: {}\n".format(idx+1, option, current.options[option])
                        indexes[idx] = option
                else:
                    for idx, option in current.options:
                        result += "[{}] {}\n".format(idx+1, option)
                await menuMsg.edit(content=result + "\nPick an option.```")
                reply = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.bot.user and m.content.isdigit() and m.channel == ctx.message.channel)
                await reply.delete()
                if type(current.options) == dict:
                    current.inputFunction(reply, indexes[int(reply.content)-1])
                else:
                    current.inputFunction(reply, current.options[int(reply.content)-1]) 
                    
                if not current.leadsTo:
                    break
                    
                current = current.leadsTo
                    