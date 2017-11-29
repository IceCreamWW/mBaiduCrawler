
*	**目录**
	*	[使用说明](#instruction)
	*	[字典和标记](#user_json)
		*	[user.json 示例](#user_json_example)
	*	[并行和规则](#common_json)
		*	[common.json 示例](#common_json_example)
	*	[依赖的库](#dependencies)
	*	[已知的bug](#exceptions)
	
___

<div id='instruction'></div>

### 使用说明

按照参数说明配置 **词典文件** 和 **标记方式**, 运行 **main.py**

**仓库中的词典和标记是一组可以运行的配置**。

___

<div id='user_json'></div>

### 字典和标记（user.json 参数说明）
*	**keyword-file-dir**
	*	词库目录
	*	程序会扫描这个文件夹下的[词典](#1)(仅一层)
	*	词典格式：以换行符分割的单词

*	**keyword-file-ext**
	*	词库文件扩展名
	*	词库文件下，以这个扩展名为后缀的词库会被认为是词典

*	**keyword-mark-map**
	* 	词库标记映射（字典类型）
	*	词库文件除后缀之外的文件名为键，标记符号为值

*	**keyword-hint-map**
	*	搜索时用到的提示词（字典类型key，value）
	*	搜索时会输入 keyword value
	*	可以是**任何有利于限制搜索范围的值**
	*	如
		*	"人名": "是谁？"
*	**mark**
	*	所有标记都具有的特征，被用于确定一个文件中的标记数量

*	**min/max-keyword-length**
	*	筛选关键词时的限制长度

___

### user.json 示例

<div id='user_json_example'></div>

```json
{
	"keyword-file-dir": ".\\词库",
	"keyword-file-ext": ".lexicon",
	"keyword-mark-map":
	{
	"医院": "M1",
	"疾病": "M2",
	"科室": "M3",
	"药品": "M4",
	"症状": "M5"

	},
	"keyword-hint-map":
	{
	"医院": "医院",
	"疾病": "病因",
	"科室": "科室",
	"药品": "药",
	"症状": "症状"
	},
	"mark": "M",
	"min-keyword-length" : 2,
	"max-keyword-length" : 20
}

```

___

<div id="common_json"></div>

### 并行和规则（common.json参数说明）

*	**ban-urls**
	*	含有这个列表内容的网址不会被爬取
	*	通常是因为
		*	它们以视频或图片为主
		*	已知它们的主要内容通过ajax加载

*	**user-agents**
	*	随机使用的user-agents，通常是不需要的

*	**max-thread / max-process**
	*	线程、进程数
	*	多线程爬取网页内容
	*	多进程处理网页内容

*	**min-marks**
	*	一个网页文本应具有的最少标记数量

*	**max-page**
	*	每个关键词爬取百度结果的页数

*	min / max-contents
	*	（这一项通常不需要修改）
	*	控制爬取的网页内容队列的长度

*	check-net-interval
	*	检查网络状态的间隔，单位是秒

*	check-queue-interval
	*	检查网页队列大小的间隔，单位是秒

*	keyword-config
	*	user.json的位置和命名

*	**DEL-MARK**
	*	从标签开始到结束都需要删除
	*	典型标签为script

*	**TEXT-MARK**
	*	行内标记，替换为空而不是空格
	*	（因为它们通常只控制字体，并不区分内容含义）
___	
<div id="common_json_example"></div>

### common.json 示例
```json
{
	"ban-urls" : ["image","iqiyi","video","music"],
	"user-agents" :
	[
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
	"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
	"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"
	],
	"max-thread" : 10,
	"max-process" : 2,
	"min-marks" : 2,
   	"min-contents" : 50,
	"max-contents" : 100,
	"max-urls" : 10000000,
	"err-rate" : 0.01,
	"max-page" : 2,
	"check-net-interval" : 20,
	"check-queue-interval" : 5,
	"timeout" : 10,
	"keyword-config" : ".\\user.json",
	"TEXT-MARK" : ["strong", "p", "b", "em", "s", "l", "a", "h1", "h2", "h3", "span"],
	"DEL-MARK" : ["button", "script", "style"]
  
}
```

___
<div id="dependencies"></div>

### 依赖的库

*	bs4
*	requests
*	pybloom_live

___
<div id="exceptions"></div>

### 已知的问题

*	urlgenerator 不会因为其中的内容大量积存而暂停，导致如果爬取量过大，会占用1G以上内存
