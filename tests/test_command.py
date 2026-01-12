from peaty.cmd import Command

cmd = Command.from_raw("ls -l")
print(cmd)
res = cmd.run()
print(res)
