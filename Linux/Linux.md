 Linux

[toc]

# 前言

##  `Linux` 主要目录速查表

> /etc/passwd 用戶库
>
> /etc/shadow 密码库
>
> /etc/group 组账号基本信息
>
> /etc/gshadow 组账号密码信息

- /：根目录，

  一般根目录下只存放目录，在 linux 下有且只有一个根目录，所有的东西都是从这里开始

  - 当在终端里输入 `/home`，其实是在告诉电脑，先从 `/`（根目录）开始，再进入到 `home` 目录

- /bin、/usr/bin：可执行二进制文件的目录，如常用的命令 ls、tar、mv、cat 等

- /boot：放置 linux 系统启动时用到的一些文件，如 linux 的内核文件：`/boot/vmlinuz`，系统引导管理器：`/boot/grub`

- **/dev：存放linux系统下的设备文件，访问该目录下某个文件，相当于访问某个设备，常用的是挂载光驱`mount /dev/cdrom /mnt`**

  > 硬件都在/dev 目录，如**硬盘、U盘为/dev/sd[a-d]； /dev/sr0（/dev/cdrom）是光驱的设备名（df命令查看）**，为设备文件，代表的是光驱本身，**得把这个设备挂载到目录下（一般为/mnt）(文件系统的临时挂载点)，才能对设备上的文件进行读写等操作；**

- **/etc：系统配置文件存放的目录**，不建议在此目录下存放可执行文件，重要的配置文件有

  - /etc/inittab
  - /etc/fstab
  - /etc/init.d
  - /etc/X11
  - /etc/sysconfig
  - /etc/xinetd.d

- /home：系统默认的用户家目录，新增用户账号时，用户的家目录都存放在此目录下

  - **`~` 表示当前用户的家目录，会进到/home/当前用户里**

    > **而/home表示的是包含所有用户家目录的一个目录**

  - `~edu` 表示用户 `edu` 的家目录

- **/lib、/usr/lib、/usr/local/lib：系统使用的函数库的目录，程序在执行过程中，需要调用一些额外的参数时需要函数库的协助**

- /lost+fount：系统异常产生错误时，会将一些遗失的片段放置于此目录下

- **/mnt: /media：光盘默认挂载点，通常光盘挂载于 /mnt/cdrom 下，也不一定，可以选择任意位置进行挂载**

- **/opt：给主机额外安装软件所摆放的目录**

- /proc：此目录的数据都在内存中，如系统核心，外部设备，网络状态，由于数据都存放于内存中，所以不占用磁盘空间，比较重要的文件有：/proc/cpuinfo、/proc/interrupts、/proc/dma、/proc/ioports、/proc/net/* 等

- /root：系统管理员root的家目录

- /sbin、/usr/sbin、/usr/local/sbin：放置系统管理员使用的可执行命令，如 fdisk、shutdown、mount 等。与 /bin 不同的是，这几个目录是给系统管理员 root 使用的命令，一般用户只能"查看"而不能设置和使用

- /tmp：一般用户或正在执行的程序临时存放文件的目录，任何人都可以访问，重要数据不可放置在此目录下

- /srv：服务启动之后需要访问的数据目录，如 www 服务需要访问的网页数据存放在 /srv/www 内

- /usr：应用程序存放目录

  - /usr/bin：存放应用程序
  - /usr/share：存放共享数据
  - /usr/lib：存放不能直接运行的，却是许多程序运行所必需的一些函数库文件
  - /usr/local：存放软件升级包
  - /usr/share/doc：系统说明文件存放目录
  - /usr/share/man：程序说明文件存放目录

- /var：放置系统执行过程中经常变化的文件

  - /var/log：随时更改的日志文件
  - /var/spool/mail：邮件存放的目录
  - /var/run：程序或服务启动后，其 PID 存放在该目录下

##  常用 Linux 命令的基本使用

| 序号 | 命令           | 对应英文             | 作用                     |
| ---- | -------------- | -------------------- | ------------------------ |
| 01   | ls             | list                 | 查看当前文件夹下的内容   |
| 02   | pwd            | print work directory | 查看当前所在文件夹       |
| 03   | cd [目录名]    | change directory     | 切换文件夹               |
| 04   | touch [文件名] | touch                | 如果文件不存在，新建文件 |
| 05   | mkdir [目录名] | make directory       | 创建目录                 |
| 06   | rm [文件名]    | remove               | 删除指定的文件名         |
| 07   | clear          | clear                | 清屏                     |

##  查阅命令帮助信息

> 先学习**常用命令**及**常用选项**的使用即可，工作中如果遇到问题可以借助 **网络搜索**

###  `--help`

```bash
command --help
```

- 显示 `command` 命令的帮助信息

###  man

```bash
man command
```

- 查阅 `command` 命令的使用手册

> `man` 是 **manual** 的缩写，是 Linux 提供的一个 **手册**，包含了绝大部分的命令、函数的详细使用说明
>
> **只记得关键词，可用man -k 关键词**

- 使用 `man` 时的操作键：

| 操作键       | 功能                     |
| ------------ | ------------------------ |
| **空格键**   | **显示手册页的下一屏**   |
| **Enter 键** | **一次滚动手册页的一行** |
| **b**        | 回滚一屏                 |
| f            | 前滚一屏                 |
| **q**        | 退出                     |
| **/word**    | 搜索 **word** 字符串     |

## Linux代码编写

- **Linux命令常用结构** ：`Command [-option] [argument]`
  Command：即是要运行的命令的本身，说白了就是一个软件（程序）；
  Option：是选项（可选），选项是控制命令运行状态和行为的（可多个选项一起，如df -hT）；
  Argument：是参数（可选），是命令要操作对象如文件、路径、数据、目录等；
  在指令的第一部分按[tab]键一下为[命令补全]，两下为所有命令选择，在非第一部分按[tab]键两下为[文件补全]；
- **linux命令区分大小写**；

# 文件和目录常用命令

- 查看目录内容
  - `ls`
- 切换目录
  - `cd`
- 创建和删除操作
  - `touch`
  - `rm`
  - `mkdir`
- 拷贝和移动文件
  - `cp`
  - `mv`
- 查看文件内容
  - `cat`
  - `more`
  - `grep`
- 其他
  - `echo`
  - 重定向 `>` 和 `>>`
  - 管道 `|`

##  查看目录内容ls 

- `ls` 是英文单词 **list** 的简写，其功能为列出目录的内容，是用户最常用的命令之一，类似于 **DOS** 下的 `dir` 命令

>  Linux 下文件和目录的特点
>
> - Linux **文件** 或者 **目录** 名称最长可以有 `256` 个字符
> - 以 `.` 开头的文件为隐藏文件，需要用 -a 参数才能显示
> - **.** 代表当前目录
> - **..** 代表上一级目录

| 参数 | 含义                                         |
| ---- | -------------------------------------------- |
| -a   | 显示指定目录下所有子目录与文件，包括隐藏文件 |
| -l   | 以列表方式显示文件的详细信息                 |
| -h   | 配合 -l 以人性化的方式显示文件大小           |
| -R   | 显示出目录下以及其所有子目录的文件名         |
| F    | 列出当前目录下的文件名及其类型               |
| t    | 依照文件最后修改时间的顺序列出文件           |

>  **通配符的使用**
>
> | 通配符 | 含义                                 |
> | ------ | ------------------------------------ |
> | *      | 代表任意个数个字符                   |
> | ?      | 代表任意一个字符，至少 1 个          |
> | []     | 表示可以匹配字符组中的任一一个       |
> | [abc]  | 匹配 a、b、c 中的任意一个            |
> | [a-f]  | 匹配从 a 到 f 范围内的的任意一个字符 |

##  切换目录`cd`

> pwd：显示用户当前所处的目录

- `cd` 是英文单词 **change directory** 的简写，其功能为更改当前的工作目录，也是用户最常用的命令之一

> **注意：Linux 所有的 目录 和 文件名 都是大小写敏感的**

| 命令  | 含义                                   |
| ----- | -------------------------------------- |
| cd    | 切换到当前用户的主目录(/home/用户目录) |
| cd ~  | 切换到当前用户的主目录(/home/用户目录) |
| cd .  | 保持在当前目录不变                     |
| cd .. | 切换到上级目录                         |
| cd -  | 可以在最近两次工作目录之间来回切换     |

> 相对路径和绝对路径：
>
> - **相对路径** 在输入路径时，最前面不是 **/** 或者 **~**，表示相对 **当前目录** 所在的目录位置
> - **绝对路径** 在输入路径时，最前面是 **/** 或者 **~**，表示从 **根目录/家目录** 开始的具体目录位置

##  创建/删除文件(夹)

### `touch`

- 创建文件或修改文件时间
  - 如果文件 **不存在**，可以创建一个空白文件
  - 如果文件 **已经存在**，可以修改文件的末次修改日期

###  `mkdir`

- 创建一个新的目录

| 选项 | 含义                             |
| ---- | -------------------------------- |
| -p   | 可以递归创建目录                 |
| m    | 只把文件的修改时间改为当前时间。 |

> **新建目录的名称** 不能与当前目录中 **已有的目录或文件** 同名

###  `rm`

- 删除文件或目录

> 使用 `rm` 命令要小心，因为文件删除后不能恢复

| 选项 | 含义                                                  |
| ---- | ----------------------------------------------------- |
| -f   | 强制删除，忽略不存在的文件，无需提示                  |
| -r   | 递归地删除目录下的内容，**删除文件夹** 时必须加此参数 |
| R    | 递归删除目录                                          |

###  `rmdir`

- 删除空目录

  > -p递归删

##  拷贝和移动文件

| 序号 | 命令               | 对应英文 | 作用                                 |
| ---- | ------------------ | -------- | ------------------------------------ |
| 01   | tree [目录名]      | tree     | 以树状图列出文件目录结构             |
| 02   | cp 源文件 目标文件 | copy     | 复制文件或者目录                     |
| 03   | mv 源文件 目标文件 | move     | 移动文件或者目录／文件或者目录重命名 |

###  `tree`

- `tree` 命令可以以树状图列出文件目录结构

| 选项 | 含义       |
| ---- | ---------- |
| -d   | 只显示目录 |

###  `cp`

- `cp` 命令的功能是将给出的 **文件** 或 **目录** 复制到另一个 **文件** 或 **目录** 中，相当于 **DOS** 下的 `copy` 命令

| 选项 | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| -i   | 覆盖文件前提示                                               |
| -r   | 若给出的源文件是目录文件，则 cp 将递归复制该目录下的所有子目录和文件，目标文件必须为一个目录名 |
| -R   | ：递归复制目录，即包含目录下的各级子目录。                   |
| a    | 尽可能将文件状态、权限等属性照原状予以复制。                 |
| f    | 如果目标文件或目录存在，先删除它们再进行复制（即覆盖），并且不提示用户。 |

###  `mv`

- `mv` 命令可以用来 **移动** **文件** 或 **目录**，也可以给 **文件或目录重命名**

| 选项 | 含义           |
| ---- | -------------- |
| -i   | 覆盖文件前提示 |
| f    |                |

##  查看文件内容

> - **cat [-n] 文件名** :显示文件内容，连行号一起显示
> - **less 文件名** ：一页一页的显示文件内容（搜索翻页同man命令）
> - **head [-n] 文件名** ：显示文件头n行内容，n指定显示多少行
> - **tail [-nf] 文件名**:显示文件尾几行内容,n指定显示多少行,f用于实时追踪文件的所有更新，常用于查阅正在改变的日志文件（如tail -f -n 3 a.log 表示开始显示最后3行，并在文件更新时实时追加显示，没有-n默认10行）
> - **sed -n '2,$p' ab** ：显示第二行到最后一行；
> - **sed -n '/搜索的关键词/p' a.txt** ：显示包括关键词所在行
> - **cat filename |grep abc -A10** ：查看filename中含有abc所在行后10行（A10）、前10行（B10）内容
> - **less a.txt|grep git** ：显示关键词所在行，管道符”|”它只能处理由前面一个指令传出的正确输出信息，对错误信息信息没有直接处理能力。然后传递给下一个命令，作为标准的输入；
> - **cat /etc/passwd |awk -F ':' '{print $1}'** ：显示第一列

###  `cat`

- `cat` 命令可以用来 **查看文件内容**、**创建文件**、**文件合并**、**追加文件内容** 等功能
- `cat` 会一次显示所有的内容，适合 **查看内容较少** 的文本文件

| 选项   | 含义                   |
| ------ | ---------------------- |
| -b     | 对非空输出行编号       |
| **-n** | **对输出的所有行编号** |

> Linux 中还有一个 `nl` 的命令和 `cat -b` 的效果等价

###  `more`

- `more` 命令可以用于分屏显示文件内容，每次只显示一页内容
- 适合于 **查看内容较多**的文本文件

使用 `more` 的操作键：

| 操作键   | 功能                 |
| -------- | -------------------- |
| 空格键   | 显示手册页的下一屏   |
| Enter 键 | 一次滚动手册页的一行 |
| b        | 回滚一屏             |
| f        | 前滚一屏             |
| q        | 退出                 |
| /word    | 搜索 **word** 字符串 |

###  `less`

> less可以用滚轮，more不行

​	less命令是more命令的改进版，比more命令的功能强大。more命令只能向下翻页，而less命令可以向下、向上翻页，甚至可以前后左右移动。      

​	按“Enter”回车键可以向下移动一行，按“Space”空格键可以向下移动一页，按“B”键可以向上移动一页，也可以用光标键向前、后、左、右移动，按“Q”键可以退出less命令。

###  `head`

​	  head命令用于显示文件的开头部分，默认情况下只显示文件的前10行内容。该命令的语法为:

- head  [参数]  文件名

head命令的常用参数选项如下。

**-n num：显示指定文件的前num行。**

**-c num：显示指定文件的前num个字符。**

[root@Server01 ~]#head  -n  20  /etc/passwd   //显示 passwd文件的前20行

###  `tail`

​	tail命令用于显示文件的末尾部分，默认情况下，只显示文件的末尾10行内容。该命令的语法为

- tail  [参数]  文件名

**-n num：显示指定文件的末尾num行。**

**-c num：显示指定文件的末尾num个字符。**

**+num：从第num行开始显示指定文件的内容。**

[root@Server01 ~]#tail  -n  20  /etc/passwd   //显示 passwd文件的末尾20行

##  其他

###  `echo 文字内容`

- `echo` 会在终端中显示参数指定的文字，通常会和 **重定向** 联合使用

###  重定向 `>` 和 `>>`

- Linux 允许将命令执行结果 **重定向**到一个 **文件**
- 将本应显示在**终端上的内容** **输出／追加** 到**指定文件中**

其中

- **`>` 表示输出，会覆盖文件原有的内容**
- **`>>` 表示追加，会将内容追加到已有文件的末尾**

###  管道 `|`

- Linux 允许将 **一个命令的输出** 可以**通过管道** 做为 **另一个命令的输入**
- 可以理解现实生活中的管子，管子的一头塞东西进去，另一头取出来，这里 `|` 的左右分为两端，左端塞东西（写），右端取东西（读）

常用的管道命令有：

- `more`：分屏显示内容
- `grep`：在命令执行结果的基础上查询指定的文本

### 别名

alias xxx＝“xxx” 用来设置指令的别名

## 快捷方式

> ln：link的缩写，用于建立硬（软）链接，常用于软件安装时建软链接(类似快捷方式)到PATH;
> 语法：ln [-s] 源文件 目标文件

- **ln -s /opt/a.txt /opt/git/** :对文件创建软链接（快捷方式不改名还是a.txt）

- **ln -s /opt/a.txt /opt/git/b** :（快捷方式改名为b）（下面的一样可以改名）

- **ln -s /opt/mulu /opt/git/** :对目录创建软链接

- **ln /opt/a.txt /opt/git/** :对文件创建硬链接

  > -s表示软连接 soft

## 文件查找

###  find

用于文件的查找--**用于已知文件名，不知道文件位置**

- **语法：find pathname -options [-print -exec ...]**

pathname ：为 find命令所查找的目录路径。例如用.来表示当前目录，用/来表示系统根目录（find查找范围为目标目录及其子目录所有文件及目录）；
-exec： find命令对匹配的文件执行该参数所给出的shell命令。相应命令的形式为'command' { } ;，注意{ }和；之间的空格；
-print： find命令将匹配的文件输出到标准输出；

- **find /home -mtime -2** ：在/home下查最近2*24小时内改动过的文件
- **find . -size +100M** ：在当前目录及子目录下查找大于100M的文件
- **find . -type f** ：f表示文件类型为普通文件（b/d/c/p/l/f 分别为块设备、目录、字符设备、管道、符号链接、普通文件）
- **find . -mtime +2 -exec rm {} ;** :查出更改时间在2*24小时以前的文件并删除它**
- **find . -name '\*.log' -exec grep -i hello {} \; -print** :在当前目录及子目录下查出文件名后缀为.log的文件并且该文件内容包含了hello字样并打印，-exec 命令 {} \表示对查出文件操作，-i表示不区分大小写；
- **find . -name '\*.log'|grep hello** :在当前目录及子目录下查出文件名后缀为.log的文件并且文件名包含了hello字样（grep用来处理字符串）；

> -name filename：查找指定名称的文件
>
> -user username：指定用户
>
> -group grpname
>
> -print：显示查找结果
>
> -type：查找指定类型，有b（块设备）、c（字符设备文件）、d（目录）、f（普通文件）

###  locate

用于文件的查找--**用于只知部分文件名，不知在哪里**

- **locate a.txt** ：在系统全局范围内查找文件名包含a.txt字样的文件（比find快）;

> locate:原理是updatedb会把文件系统中的信息存放到数据库databases中（但一般一天才执行一次，所以locate找不到新创建的文件，需要先手动执行updatedb，再执行locate）,locate从数据库中读数据;

> ***：表示0个或多个字符**
>
> **？：表示1个字符**
>
> -name filename：查找指定名称的文件
>
> -user username：指定用户
>
> -group grpname
>
> -print：显示查找结果
>
> -type：查找指定类型，有b（块设备）、c（字符设备文件）、d（目录）、f（普通文件）

### `grep`

```linux
grep [-inv] find_text txt
```

- Linux 系统中 `grep` 命令是一种强大的文本搜索工具
- `grep`允许对文本文件进行 **模式**查找，所谓模式查找，又被称为正则表达式，在就业班会详细讲解

| 选项 | 含义                                     |
| ---- | ---------------------------------------- |
| -n   | 显示匹配行及行号                         |
| -v   | 显示不包含匹配文本的所有行（相当于求反） |
| -i   | 忽略大小写                               |

- 常用的两种模式查找

| 参数    | 含义                         |
| ------- | ---------------------------- |
| **^a**  | **行首，搜寻以 a 开头的行**  |
| **ke$** | **行尾，搜寻以 ke 结束的行** |

- **grep -i 'HELLO' . -r -n** ：在当前目录及子目录下查找文件内容中包含hello的文件并显示文件路径（-i表示忽略大小写）

### 其他

- **which java** ：在环境变量$PATH设置的目录里查找符合条件的文件，并显示路径（查询运行文件所在路径）
- **whereis java** :查看安装的软件的所有的文件路径（whereis 只能用于查找二进制文件、源代码文件和man手册页，一般文件的定位需使用locate命令）

## 文本处理

- **ls -l>file** ：输出重定向>（改变原来系统命令的默认执行方式）：ls -l命令结果输出到file文件中，若存在，则覆盖
- **cat file1 >>file** ：输出重定向之cat命令结果输出追加到file文件
- **ls fileno 2>file** ： 2>表示重定向标准错误输出（文件不存在，报错信息保存至file文件）；
- **cowsay <a.txt** :重定向标准输入’命令<文件’表示将文件做为命令的输入（为从文件读数据作为输入）
- **sed -i '4,$d' a.txt** ：删除第四行到最后一行（$表示最后一行）（sed可以增删改查文件内容）
- **sed -i '$a 增加的字符串' a.txt** ：在最后一行的下一行增加字符串
- **sed -i 's/old/new/g' a.txt** :替换字符串；格式为sed 's/要替换的字符串/新的字符串/g' 修改的文件
- **vim 文件**：编辑查看文件（同vi）

# 开关机命令

- **sync** ：把内存中的数据写到磁盘中（关机、重启前都需先执行sync）
- **shutdown -r now**或**reboot** ：立刻重启
- **shutdown -h now** ：立刻关机
- **shutdown -h 20:00** ：预定时间关闭系统（晚上8点关机，如果现在超过8点，则明晚8点）
- **shutdown -h +10** ：预定时间关闭系统（10分钟后关机）
- **shutdown -c** ：取消按预定时间关闭系统
- reboot：重启
- halt：关机

# 系统信息

- **who am i** ：查看当前使用的终端
- **who** 或 **w** ： 查看所有终端
- whereis 命令：用来寻找命令的可执行文件所在的位置
- **uname -m** ：显示机器的处理器架构（如x86_64）
- **cat /proc/version** ：查看linux版本信息
- **uname -r** ：显示正在使用的内核版本
- **rpm -qa | grep kernel-devel** ：查看kernel-devel版本（安装软件时编译内核用，故需要保持内核版本一致性）
- **yum install -y "kernel-devel-uname-r == $(uname -r)"**：安装和Linux内核版本匹配的kernel-devel
- **date** ：显示系统日期 （date +%Y/%m/%d : 显示效果如2018/01/01）
- **date 0703145920100** ：设置时间（格式为月日时分年.秒 ）
- **clock -w** ：将时间修改保存到 BIOS
- **cal 2018** ：显示2018年的日历表
- **clear** ：清空命令行
- **ifconfig** ：显示或设置网卡（查ip等）（类似**windows中ipconfig**）
- **ping -c 3 www.baidu.com** ：测试百度与本机的连接情况（ -c 3表示测试3次）
- **cat /proc/cpuinfo** ：显示CPU的信息
- **cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l** ：查看物理CPU个数
- **cat /proc/cpuinfo| grep "cpu cores"| uniq** ：查看每个物理CPU的核数
- **cat /proc/cpuinfo| grep "processor"| wc -l** ：查看逻辑CPU个数即线程数

# 系统性能

- **top** ：动态实时显示cpu、内存、进程等使用情况（类似windows下的任务管理器）

- **top -d 2 -p 7427** ：-d为画面更新的秒数，默认5秒，-p为指定进程pid的信息

- **vmstat 2 10** ：每隔2秒采集一次服务器状态，采集10次（查看内存、io读写状态、cpu）

- **free -h** :查看系统内存及虚拟内存使用情况

- **df -h** :显示磁盘的空间使用情况

- **iostat** ：可查io读写、cpu使用情况

- **sar -u 3 5** :查看cpu使用情况（3秒一次，共5次）

- **sar -d 2 3** ：评估磁盘性能

- **ps aux|grep firefox** ：获取火狐的进程号（PID）（可查看进程占用cpu、内存百分比及进程触发指令的路径）

  > -a：显示当前控制终端的进程（包含其他用户的）。
  >
  > -u：显示进程的用户名和启动时间等信息。
  >
  > -w：宽行输出，不截取输出中的命令行。
  >
  > -l：按长格形式显示输出。
  >
  > -x：显示没有控制终端的进程。
  >
  > -e：显示所有的进程。
  >
  > -t n：显示第n个终端的进程。

- **kill -9 进程号** ：强制杀死进程

# 用户与权限

### 用户

- **useradd 用户名** ：创建用户
- **userdel -r 用户名** :删除用户：（-r表示把用户的主目录一起删除）
- **usermod -g 组名 用户名** ：修改用户的组
- **passwd [ludf] 用户名** ：用户改自己密码，不需要输入用户名，选项-d:指定空口令,-l:禁用某用户，-u解禁某用户，-f：强迫用户下次登录时修改口令
- **groupadd 组名** ：创建用户组
- **groupdel 用户组** ：删除组
- **groupmod -n 新组名 旧组名** ：修改用户组名字
- **su - 用户名**：完整的切换到一个用户环境（相当于登录）（建议用这个）（退出用户：exit）
- **su 用户名** :切换到用户的身份（环境变量等没变，导致很多命令要加上绝对路径才能执行）
- **sudo 命令** ：以root的身份执行命令（输入用户自己的密码，而su为输入要切换用户的密码，普通用户需设置/etc/sudoers才可用sudo）

### 文件权限

- **chmod [-R] 777文件或目录** ：设置权限（chmod a+rwx a=chmod ugo +rwx a=chmod 777 a）

  > 注： r（read）对应4，w（write）对应2，x（execute）执行对应1；
  > -R：递归更改文件属组，就是在更改某个目录文件的属组时，如果加上-R的参数，那么该目录下的所有文件的属组都会更改）

- **chmod [{ugoa}{+-=}{rwx}][文件或目录]** ：如chmod u-w,g+x,o=r test.txt为user（拥有者）去掉写权限，group(所属组)加上执行权限，other(其他人)权限等于只读；

- **chown [-R] admin:root /opt/** ：变更文件及目录的拥有者和所属组（-R递归处理所有文件和文件夹，admin为拥有者，root为所属者）

# 磁盘管理

- **df -h** :显示磁盘的空间使用情况 及挂载点
- **df -h /var/log** :（显示log所在分区（挂载点）、目录所在磁盘及可用的磁盘容量）
- **du -sm /var/log/\* | sort -rn** : 根据占用磁盘空间大小排序（MB）某目录下文件和目录大小
- **fdisk -l** :查所有分区及总容量，加/dev/sda为查硬盘a的分区）
- **fdisk /dev/sdb** :对硬盘sdb进行分区
- **mount /dev/sda1 /mnt** ：硬盘sda1挂载到/mnt目录（mount 装置文件名 挂载点）
- **mount -t cifs -o username=luolanguo,password=win用户账号密码,vers=0 //10.178/G /mnt/usb** :远程linux 共享挂载windows的U盘,G为U盘共享名，需设置U盘共享
- **mount -o loop /opt/soft/CentOS-7-x86_64-DVD-170iso /media/CentOS** ：挂载iso文件
- **umount /dev/sda1** ：取消挂载（umount 装置文件名或挂载点）

# 压缩、解压和打包备份

>  单纯tar仅为打包（多个文件包成一个大文件），加上参数-j(bzip2格式.bz2)、-z（gzip格式.gz）可以备份、压缩(-c)、解压（-x），备份一般比压缩多加参数-p（保留原本文件的权限与属性），-C可以指定解压到特定目录；bzip2、gzip只能对单一文件压缩；

- **file 文件名** ：查文件类型（可看是用哪一种方式压缩的）
- **tar -zxvf a.tar.gz -C   ./test** ：解压tar.gz到当前目录下的test目录
- **tar -zcvf /opt/c.tar.gz   ./a/** ：压缩tar.gz（把当前目录下的a目录及目录下所有文件压缩为 /opt/目录下的c.tar.gz）
- **tar -jxvf a.tar.bz2** ：解压tar.bz2（到当前目录）
- **tar -jcvf c.tar.bz2 ./a/** ：压缩tar.bz2（把当前目录下的a目录及目录下所有文件压缩到当前目录下为c.tar.gz2）
- **unzip a.zip** ：解压zip（到当前目录）
- **zip -r c.zip ./a/** :压缩zip(把当前目录下的a目录及目录下所有文件压缩到当前目录下为c.zip
- **bzip2 -k file1** ： 压缩一个 'file1' 的文件（-k表示保留源文件）（bzip2格式，比gzip好）
- **bzip2 -d -k filebz2** ： 解压一个叫做 'filebz2'的文件
- **gzip file1** ： 压缩一个叫做 'file1'的文件（gzip格式）（不能保留源文件）
- **gzip -9 file1** ： 最大程度压缩
- **gzip -d filegz** ： 解压缩一个叫做 'file1'的文件

# 软件安装

> - **尽量用yum源（apt-get）安装，不行就rpm、deb包安装，能不手动编译的就不要手动编译；**
> - dpkg只能安装已经下载到本地机器上的deb包. apt-get能在线下载并安装deb包,能更新系统,且还能自动处理包与包之间的依赖问题,这个是dpkg工具所不具备的；
> - **rpm 只能安装已经下载到本地机器上的rpm 包. yum能在线下载并安装rpm包,能更新系统,且还能自动处理包与包之间的依赖问题**,这个是rpm 工具所不具备的;
> - yum、rpm安装文件分布在/usr的bin、lib、share不同目录，不用配置PATH，直接用命令，但可用命令卸载更新；
> - 手动编译软件，默认位置为/usr/local下不同子目录下,不用配置PATH直接用命令（手动指定安装路径需要加PATH），使得软件更新和删除变得很麻烦。编译安装的软件没有卸载命令，卸载就是把所有这个软件的文件删除。

## 二进制(Binaries)包

### yum安装

>  在线下载并安装rpm包，适用于CentOS、Fedora、RedHat及类似系统

- **yum install epel-releas** ：安装第三方yum源EPEL（企业版 Linux 附加软件包的简称）
- **yum repolist enabled** ：显示可用的源仓库（/etc/yum.repos.d/目录下配置）
- **yum install yum-fastestmirror** ：自动选择最快的yum源
- **yum list installed |grep java** ：列出已安装的软件（查看已安装的JDK）
- **yum remove java-0-openjdk.x86_64** ：卸载软件（卸载JDK）
- **yum list java\*** ：列出已安装和可安装的软件（查看yum库中的JDK包）
- **yum install [-y] java-0-openjdk** ：安装软件JDK(-y自动安装)（推荐这种方式安装）
- **yum check-update [kernel]** ：列出所有可更新的软件（检查更新kernel）
- **yum update tomcat** ：更新软件（可所有）
- **rpm -ql 软件名称** ：查询yum安装路径（软件名称可通过rpm -qa|grep java）
- **yum info kernel** ：查看软件（kernel）的信息
- **yum clean all** ：（清除缓存，使最新的yum配置生效）

### rpm包手动下载安装

>  yum中没有时用，适用于CentOS、Fedora、RedHat及类似系统；

- **wget -P /opt https://网址** ：下载到/opt目录
- **rpm -ivh wps-office-版本.x86_6rpm** :安装rpm包（包要先下载）（要先装依赖包）
- **rpm -e wps-office** ：卸载软件（注意不要软件名不要版本号）
- **rpm -qa |grep wps** ：查看安装的rpm包
- **rpm -ql 软件名称** ：查看rpm包安装路径（软件名称可通过rpm -qa|grep java）

### apt方式安装

>  安装deb包，类似yum安装，适用于Debian, Ubuntu 以及类似系统；

- **apt-get install aptitude** ：安装aptitude工具,实现依赖自动安装，依赖版本自动降级或升级
- **aptitude install 软件** ：安装软件（推荐这种方式安装）
- **apt-cache search 软件** ：搜索软件
- **apt-get install 软件** ：安装软件
- **apt-get purge 软件** ：卸载软件（包括配置文件，只删除软件purge换成remove）
- **apt-get upgrade** ：更新所有已安装的软件包
- **apt-get update** ：升级列表中的软件包
- **apt-get clean** ：从下载的软件包中清理缓存

### deb包安装

>  适用于Debian, Ubuntu 以及类似系统；

- **dpkg -i package.deb** ：安装一个 deb 包
- **dpkg -r package_name** ：从系统删除一个 deb 包
- **dpkg -l |grep chrome** ：查询系统中所有已经安装的 deb 包
- **dpkg -L 软件名称** ：查软件安装的文件

### 解压即用

>  大多数非开源的商业软件都采取这种办法；

 二进制（Binaries）包如[apache-jmeter-tgz](https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-tgz)，下载复制解压到/opt，然后然后将该软件的 bin 目录加入到 PATH 中即可（vim /etc/profile export PATH=$PATH:/opt/apache-jmeter-3/bin）；

### 软件自己的模块/包管理器

>  如python：系统的源中不可能包含该软件的所有模块； 系统的源中该软件的模块的更新要远远滞后于最新版本；手动安装python，并用Python 自带的 pip 安装模块（类似yum）；

- **pip install redis** ：安装python软件包[redis](http://www.ttlsa.com/redis/)
- **pip unstall redis** :卸载
- **pip show --files redis** :pip查看已安装的包
- **pip list --outdated** :检查更新

## 源代码(Source)包

### 编译安装

>  源代码包（一般有install文件）如[hello-tar.bz2](http://ftp.gnu.org/gnu/hello/hello-tar.bz2)，下载复制到/opt;

- **tar -jxvf hello-tar.bz2** :解压
- **./configure --prefix=/opt/软件目录名称** :为编译做好准备，加上 prefix 手动指定安装路径
- **make** ：编译
- **make install** ：安装
- **make clean** ：删除安装时产生的临时文件
- **vim /etc/profile export PATH=$PATH:/opt/目录/bin** ：手动指定安装路径需要加path
- **hello** ：执行软件：看INSTALL和README文件（是否源码包、如何安装、执行都看这两个）
- **rm -rf 软件目录名称** :卸载软件

# Vim常用命令

- 三种模式：

## 插入模式（Insert）

- ### 输入


```python
i		#在当前位置前插入
I		#在当前首行插入
a		#在当前位置之后插入一行
A		#在当前之后插入一行
o		#在当前行之后插入一行
O		#在当前行之后插入一行
```

## 命令行模式（Esc）

**按v选中需要复制内容（Shift键加v选择一行）再按y复制 p粘贴**

- gg 光标移到文档第一行
- G 光标移到最后一行
- H 光标移到当前屏幕第一行
- M 光标移到当前屏幕中间那一行
- L 光标移到当前屏幕最后一行
- home键 跳到行首
- end键 跳到行尾
- w 光标跳到下一个单词首
- xl 光标跳到x个字符
- **x,X：在一行字中，x 为向后删除一个字符（相当于[Del]键），X 为向前删除一个字符（相当于[Backspace]）。**
- **dd：删除光标所在的一整行。**
- **ndd：删除光标所在的向下 n 行。**
- **yy：复制光标所在的一行。**
- **nyy：复制光标所在的向下 n 行。**
- **p,P：p 为将已复制的内容在光标的下一行粘贴，P 则为粘贴在光标的上一行。**

### 进行操作的移动

```python
h		#左移一个字符
j		#下移一个字符
k		#上移一个字符
l		#右移一个字符
```

**以上四个命令可以配合数字使用，比如20j就是向下移动20行，5h就是向左移动5个字符。**

### 编辑

```python
u			#撤销
Ctrl+r		#重做
yy			#复制当前行
按v（逐字）或V（逐行）进入可视模式，然后用jklh命令移动即可选择某些行或字符，再按y即可复制任意部分
p 			#粘贴在当前位置
另外，删除在vim里面就是剪切的意思，所以dd就是剪切当前行，可以用v或V选择特定部分再按d就是任意剪切了
```

### 删除

```python 
dd		#删除当前行
dj		#删除当前行和上一行
dk		#删除当前行及下一行
10dd	#删除当前行开始的共10行
D		#删除当前字符至末尾
```

### 跳转

```python
gg		#跳转到文件头
G		#跳转到文件尾
gg=G	#自动缩进(非常有用)
Ctrl+d	#向下滚动半屏
Ctrl+u	#向上滚动半屏
Ctrl+f	#向下滚动半屏
Ctrl+b	#向上滚动半屏
：120	#跳转到120行
$		#跳转到行首
0		#跳转到行尾
```

## 末行模式（按“ ：”键）

- **:e 文件名 在末行模式下（打开并编辑指定名称的文件）**
- **:r 文件名 在末行模式下（在当前文件插入其它文件内容）**
- :s /old/new 将当前行中查找到的第一个字符"old" 串替换为 "new"
- **:s /old/new/g 将当前行中查找到的所有字符串“old” 替换为“new**
- :x，x s/old/new/g 在行号 “x，x” 范 围内替换所有的字符串“old”为“new&apos;
- **:% s/old/new/g 在整个文件范围内替换所有的字符串“old”为 “new”**
- :w xxx(文件名） 将这个文件另存为
- **:? ww 在文件内容中查找ww**
- **:/ww 在文件内容中查找ww N:上一个 n:下一个**

### 打开/退出

```python
vim -R file1	#只读打开
：qall		#推出所有文件
:wq			#写入退出
：q!			#强制退出
ZZ    #保存退出
```

### 查找和替换：

```python
按 vi 进入文件后，可进行以下操作进行查找和替换

/lemon：向下寻找一个名称为 #lemon 的字符串。

?lemon：向上寻找一个名称为 #lemon 的字符串。

:n1,n2s/lemon1/lemon2/g：#在第 n1 行和 n2 行之间寻找 lemon1 这个字符串，并且将其替换为 lemon2.

:1,$s/lemon1/lemon2/g：#从第一行到最后一行寻找 lemon1 这个字符串，并且将其替换为 lemon2.

:1,$s/lemon1/lemon2/gc：#从第一行到最后一行寻找 lemon1 这个字符串，并且将其替换为 lemon2.且在替换前显示提示字符给用户确认是否需要替换。
```



### 查找

```python
/text		#查找text,按n键查找下一个，按N键查找前一个
？text		#查找text,反向查找，按n键查找下一个，按N键查找前一个
:set ignorecase　　#忽略大小写的查找
:set noignorecase　　#不忽略大小写的查找
```

### 替换

```python
:s/old/new/		#用new替换old,替换当前行的第一个匹配的
:s/old/new/g	#用new替换old,替换当前行的所有匹配
:%s/old/new/ 	#用new替换old，替换所有行的第一个匹配
:%s/old/new/g 	#用new替换old，替换整个文件的所有匹配
    
也可以用v或V选择指定行，然后执行
```

# shell脚本

* Shell 是一个用 C 语言编写的程序，它是用户使用 Linux 的桥梁。Shell 既是一种命令语言，又是一种程序设计语言。

* Shell 是指一种应用程序，这个应用程序提供了一个界面，用户通过这个界面访问操作系统内核的服务。

* Ken Thompson 的 sh 是第一种 Unix Shell，Windows Explorer 是一个典型的图形界面 Shell。

  > **Shell是一个命令行解释器**，它为用户提供了一个向Linux内核发送请求以便裕兴程序的界面系统级程序，用户可以用Shell来启动、挂起、停止甚至是编写一些程序。

## 变量

> **定义变量:**
>
> ```
> country="China"
> Number=100
> ```
>
> 注意: **1,变量名和等号之间不能有空格;**
>
> **2,首个字符必须为字母（a-z，A-Z）。**
>
> **3, 中间不能有空格，可以使用下划线（_）。**
>
> **4, 不能使用标点符号。**
>
> **5, 不能使用bash里的关键字（可用help命令查看保留关键字）。**
>
> **使用变量:**
>
> 只需要在一个定义过的变量前面加上**美元符号 $** 就可以了, 另外,**对于变量的{} 是可以选择的, 它的目的为帮助解释器识别变量的边界**.
>
> ```
> country="China"
> 
> echo $country
> echo ${country}
> echo "I love my ${country}abcd!"   
> ```
>
> **重定义变量：** 直接把变量重新像开始定义的那样子赋值就可以了：
>
> ```
> country="China"
> country="ribenguizi"
> ```
>
> **只读变量**: 用 **readonly 命令 可以把变量字义为只读变量。**
>
> ```
> readonly country="China"
> #或
> country="China"
> readonly country
> ```
>
> **删除变量: 使用unset命令可以删除变量**，但是不能删除只读的变量。用法：
>
> ```
> unset variable_name
> ```
>
> #### 变量类型
>
> 运行shell时，会同时存在三种变量：
>
> ###### 1) 局部变量
>
> 局部变量在脚本或命令中定义，仅在当前shell实例中有效，其他shell启动的程序不能访问局部变量。
>
> ###### 2) 环境变量
>
> 所有的程序，包括shell启动的程序，都能访问环境变量，有些程序需要环境变量来保证其正常运行。必要的时候shell脚本也可以定义环境变量。
>
> ###### 3) shell变量
>
> shell变量是由shell程序设置的特殊变量。shell变量中有一部分是环境变量，有一部分是局部变量，这些变量保证了shell的正常运行
>
> 
>
> **特殊变量:**
>
> [![image](https://images201cnblogs.com/blog/961754/201703/961754-20170330200924617-39830017png)](http://images201cnblogs.com/blog/961754/201703/961754-20170330200923742-131483442png)
>
> $* 和 $@ 的区别为: $* 和 $@ 都表示传递给函数或脚本的所有参数，不被双引号(" ")包含时，都以"$1" "$2" … "$n" 的形式输出所有参数。但是当它们被双引号(" ")包含时，"$*" 会将所有的参数作为一个整体，以"$1 $2 … $n"的形式输出所有参数；"$@" 会将各个参数分开，以"$1" "$2" … "$n" 的形式输出所有参数。
>
> $? 可以获取上一个命令的退出状态。所谓退出状态，就是上一个命令执行后的返回结果。退出状态是一个数字，一般情况下，大部分命令执行成功会返回 0，失败返回 1。

 

## Shell中的替换

> **转义符：**
>
> 在echo中可以用于的转义符有：
>
> [![image](https://images201cnblogs.com/blog/961754/201703/961754-20170330200926508-106825877png)](http://images201cnblogs.com/blog/961754/201703/961754-20170330200925055-197630023png)
>
> 使用 echo 命令的 –E 选项禁止转义，默认也是不转义的； 使用 –n 选项可以禁止插入换行符；
>
> 使用 echo 命令的 –e 选项可以对转义字符进行替换。
>
> 另外，注意，经过我的实验，得到：
>
> ```
> echo "\\"        #得到 \
> echo -e "\\"   #得到  \
> 
> echo "\\\\"        #得到 \\
> echo -e "\\"       #得到  \
> ```
>
> **命令替换:**
>
> 它的意思就是说我们把一个命令的输出赋值给一个变量,方法为把命令用反引号(在Esc下方)引起来.  比如:
>
> ```
> directory=`pwd`
> echo $directory
> ```
>
> **变量替换**:
>
> 可以根据变量的状态（是否为空、是否定义等）来改变它的值.
>
> [![image](https://images201cnblogs.com/blog/961754/201703/961754-20170330200927399-399981890.png)](http://images201cnblogs.com/blog/961754/201703/961754-20170330200927008-141730691png)

 

## Shell运算符

> **算数运算符:**
>
> 原生bash不支持简单的数学运算，但是可以通过其他命令来实现，例如 awk 和 expr. 下面使用expr进行；  expr是一款表达式计算工具，使用它可以完成表达式的求值操作；
>
> [![image](https://images201cnblogs.com/blog/961754/201703/961754-20170330200928242-117458915png)](http://images201cnblogs.com/blog/961754/201703/961754-20170330200927883-112048255png)
>
> 比如：
>
> ```
> a=10
> b=20
> expr $a + $b
> expr $a - $b
> expr $a \* $b
> expr $a / $b
> expr $a % $b
> a=$b
> ```
>
> 注意:  在expr中的乖号为：\*
>
> \ 在 expr中的 表达式与运算符之间要有空格，否则错误；
>
> \ 在[ $a == $b ]与[ $a != $b ]中，要需要在方括号与变量以及变量与运算符之间也需要有括号， 否则为错误的。（亲测过）
>
> **关系运算符：**
>
> 只支持数字，不支持字符串，除非字符串的值是数字。常见的有：
>
> [![image](https://images201cnblogs.com/blog/961754/201703/961754-20170330200929336-117159089png)](http://images201cnblogs.com/blog/961754/201703/961754-20170330200928617-149032720png)
>
> 注意：也别忘记了空格；
>
> **布尔运算符：**
>
> [![image](https://images201cnblogs.com/blog/961754/201703/961754-20170330200930149-1830713780.png)](http://images201cnblogs.com/blog/961754/201703/961754-20170330200929711-87788915png)
>
> **字符串运算符：**
>
> [![image](https://images201cnblogs.com/blog/961754/201703/961754-20170330200931055-67996925png)](http://images201cnblogs.com/blog/961754/201703/961754-20170330200930617-162117848png)
>
> **文件测试运算符:**
>
> 检测 Unix 文件的各种属性。
>
> [![image](https://images201cnblogs.com/blog/961754/201703/961754-20170330200931883-296704040.png)](http://images201cnblogs.com/blog/961754/201703/961754-20170330200931477-8975312png)

 

## Shell中的字符串

> **单引号的限制：**
>
> 1. 单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的；
> 2. 单引号字串中不能出现单引号（对单引号使用转义符后也不行）。
>
> **双引号的优点：**
>
> 1. 双引号里可以有变量
> 2. 双引号里可以出现转义字符
>
> #### 拼接字符串：
>
> ```
> country="China"
> echo "hello, $country"
> #也可以
> echo "hello, "$country" "
> ```
>
> #### #获取字符串长度:
>
> ```
> string="abcd"
> echo ${#string} #输出 4
> ```
>
> #### 提取子字符串（切片）:
>
> ```
> string="alibaba is a great company"
> echo ${string:1:4} #输出liba
> ```
>
> **查找子字符串:**
>
> ```
> string="alibaba is a great company"
> echo `expr index "$string" is`
> ```
>
> 
>
> #### 处理路经的字符串：
>
> 例如：当一个路径为 /home/xiaoming/txt时，如何怎么它的路径（不带文件) 和如何得到它的文件名？？
>
> 得到文件名使用 bashname命令：  
>
> ```
> #  参数：
> #  -a,表示处理多个路径；
> # -s, 用于去掉指定的文件的后缀名；
> 
>  basename /home/yin/txt          -> txt
> 
>  basename -a /home/yin/txt /home/zhai/sh     -> 
> txt
> sh basename -s .txt /home/yin/txt    -> 1
>  basename /home/yin/txt .txt       -> 1
> ```
>
> 得到路径名（不带文件名）使用 dirname命令：
>
> ```
> 参数：没有啥参数；
> 
> //例子：
>  dirname /usr/bin/          -> /usr
>  dirname dir1/str dir2/str  -> 
> dir1
> dir2
>  dirname stdio.h            -> .
> ```

## Shell的数组:

> bash支持一维数组, 不支持多维数组, 它的下标从0开始编号. 用下标[n] 获取数组元素；
>
> **定义数组：**
>
> 在shell中用括号表示数组，元素用空格分开。 如：
>
> ```
> array_name=(value0 value1 value2 value3)
> ```
>
> 也可以单独定义数组的各个分量，可以不使用连续的下标，而且下标的范围没有限制。如：
>
> ```
> array_name[0]=value0
> array_name[1]=value1
> array_name[2]=value2
> ```
>
> **读取数组：**
>
> 读取某个下标的元素一般格式为:
>
> ```
> ${array_name[index]}
> ```
>
> 读取数组的全部元素，用@或*
>
> ```
> ${array_name[*]}
> ${array_name[@]}
> ```
>
> **获取数组的信息：**
>
> 取得数组元素的个数：
>
> ```
> length=${#array_name[@]}
> #或
> length=${#array_name[*]}
> ```
>
> 获取数组的下标：
>
> ```
> length=${!array_name[@]}
> #或
> length=${!array_name[*]}
> ```
>
> 取得数组单个元素的长度:
>
> ```
> lengthn=${#array_name[n]}
> ```

 

## printf函数：

> 它与c语言中的printf相似，不过也有不同，下面列出它的不同的地方：
>
> 1. printf 命令不用加括号
> 2. format-string 可以没有引号，但最好加上，单引号双引号均可。
> 3. 参数多于格式控制符(%)时，format-string 可以重用，可以将所有参数都转换。
> 4. arguments 使用空格分隔，不用逗号。
>
> 下面为例子：
>
> ```
> # format-string为双引号
> $ printf "%d %s\n" 1 "abc"
> 1 abc
> # 单引号与双引号效果一样 
> $ printf '%d %s\n' 1 "abc" 
> 1 abc
> # 没有引号也可以输出
> $ printf %s abcdef
> abcdef
> # 格式只指定了一个参数，但多出的参数仍然会按照该格式输出，format-string 被重用
> $ printf %s abc def
> abcdef
> $ printf "%s\n" abc def
> abc
> def
> $ printf "%s %s %s\n" a b c d e f g h i j
> a b c
> d e f
> g h i
> j
> # 如果没有 arguments，那么 %s 用NULL代替，%d 用 0 代替
> $ printf "%s and %d \n" 
> and 0
> # 如果以 %d 的格式来显示字符串，那么会有警告，提示无效的数字，此时默认置为 0
> $ printf "The first program always prints'%s,%d\n'" Hello Shell
> -bash: printf: Shell: invalid number
> The first program always prints 'Hello,0'
> $ 
> ```

## Shell中条件语句

> #### if 语句
>
> 包括：1， if [ 表达式 ] then  语句  fi
>
> \ if [ 表达式 ] then 语句 else 语句 fi
>
> \  if [ 表达式] then 语句  elif[ 表达式 ] then 语句 elif[ 表达式 ] then 语句   …… fi
>
> 例子：
>
> ```
> a=10
> b=20
> if [ $a == $b ]
> then
> echo "a is equal to b"
> else
> echo "a is not equal to b"
> fi
> ```
>
> 另外：if ... else 语句也可以写成一行，以命令的方式来运行，像这样：
>
> ```
> if test $[2*3] -eq $[1+5]; then echo 'The two numbers are equal!'; fi;
> ```
>
> 其中，test 命令用于检查某个条件是否成立，与方括号([ ])类似。
>
> **case …… esac语句**
>
> case ... esac 与其他语言中的 switch ... case 语句类似，是一种多分枝选择结构。case语句格式如下：
>
> ```
> case 值 in
> 模式1)
>  command1
>  command2
>  command3
>  ;;
> 模式2）
>  command1
>  command2
>  command3
>  ;;
> *)
>  command1
>  command2
>  command3
>  ;;
> esac
> ```
>
> 其中，  取值后面必须为关键字 in，每一模式必须以右括号结束。取值可以为变量或常数。匹配发现取值符合某一模式后，其间所有命令开始执行直至 ;;。;; 与其他语言中的 break 类似，意思是跳到整个 case 语句的最后。 如果无一匹配模式，使用星号 * 捕获该值，再执行后面的命令。

 

## Shell 的循环语句

> **for 循环** 
>
> 一般格式为：
>
> ```
> for 变量 in 列表
> do
>  command1
>  command2
>  ...
>  commandN
> done
> ```
>
> 注意：列表是一组值（数字、字符串等）组成的序列，每个值通过空格分隔。每循环一次，就将列表中的下一个值赋给变量。       例如：
>
> 顺序输出当前列表的数字：
>
> ```
> for loop in 1 2 3 4 5
> do
>  echo "The value is: $loop"
> done
> ```
>
> 显示主目录下以 .bash 开头的文件：
>
> ```
> #!/bin/bash
> for FILE in $HOME/.bash*
> do
> echo $FILE
> done
> ```
>
> **while循环**
>
> **一般格式为：**
>
> ```
> while command
> do
> Statement(s) to be executed if command is true
> done
> ```
>
> 例如：
>
> ```
> COUNTER=0
> while [ $COUNTER -lt 5 ]
> do
>  COUNTER='expr $COUNTER+1'
>  echo $COUNTER
> done
> ```
>
> **until 循环**
>
> until 循环执行一系列命令直至条件为 true 时停止。until 循环与 while 循环在处理方式上刚好相反。    常用格式为：
>
> ```
> until command
> do
> Statement(s) to be executed until command is true
> done
> ```
>
> command 一般为条件表达式，如果返回值为 false，则继续执行循环体内的语句，否则跳出循环。
>
> 
>
> 类似地， 在循环中使用 break 与continue 跳出循环。    另外，break 命令后面还可以跟一个整数，表示跳出第几层循环。

 

Shell函数

> Shell函数必须先定义后使用，定义如下，
>
> ```
> function_name () {
>  list of commands
>  [ return value ]
> }
> ```
>
> 也可以加上function关键字：
>
> ```
> function function_name () {
>  list of commands
>  [ return value ]
> }
> ```
>
> 注意: 调用函数只需要给出函数名，不需要加括号。
>
> \ 函数返回值，可以显式增加return语句；如果不加，会将最后一条命令运行结果作为返回值。
>
> \ Shell 函数返回值只能是整数，一般用来表示函数执行成功与否，0表示成功，其他值表示失败。
>
> \ 函数的参数可以通过 $n  得到.如:
>
> 
>
> ```
> funWithParam(){
>  echo "The value of the first parameter is $1 !"
>  echo "The value of the second parameter is $2 !"
>  echo "The value of the tenth parameter is ${10} !"
>  echo "The value of the eleventh parameter is ${11} !"
>  echo "The amount of the parameters is $# !"  # 参数个数
>  echo "The string of the parameters is $* !"  # 传递给函数的所有参数
> }
> funWithParam 1 2 3 4 5 6 7 8 9 34 73
> ```
>
> \ 
>
> 像删除变量一样，删除函数也可以使用 unset 命令，不过要加上 .f 选项，如下所示：
>
> ```
> unset .f function_name
> ```

 

## shell的文件包含：

> Shell 也可以包含外部脚本，将外部脚本的内容合并到当前脚本。使用：
>
> ```
> . filename
> #或
> source filename
> ```
>
> \ 两种方式的效果相同，简单起见，一般使用点号(.)，但是注意点号(.)和文件名中间有一空格。
>
> \ 被包含脚本不需要有执行权限。