name_to_id = {
	'Running': 0,
	'Waiting': 1,
	'System Error': 2,
	'SPJ Judgement Failed': 3,
	'Compile Error': 4,
	'Compilation Passed': 5,
	'Wrong Answer': 6,
	'Output Limit Exceeded': 7,
	'Time Limit Exceeded': 8,
	'Memory Limit Exceeded': 9,
	'Runtime Error': 10,
	'Partially Accepted': 11,
	'Accepted': 12,
	'Skipped': 13
}
id_to_info = {
	0: {
		'name': 'Running',
		'sign': 'fa fa-fw fa-spinner fa-spin',
		'color': '#66ccff'
	},
	1: {
		'name': 'Waiting',
		'sign': 'fa fa-fw fa-spinner fa-spin',
		'color': '#aaa'
	},
	2: {
		'name': 'System Error',
		'sign': 'fa fa-fw fa-smile-o',
		'color': '#ff0000'
	},
	3: {
		'name': 'SPJ Judgement Failed',
		'sign': 'fa fa-fw fa-smile-o',
		'color': '#ff0000'
	},
	4: {
		'name': 'Compile Error',
		'sign': 'fa fa-fw fa-code',
		'color': '#ede42b'
	},
	5: {
		'name': 'Compilation Passed',
		'sign': 'fa fa-fw fa-check',
		'color': '#19d960'
	},
	6: {
		'name': 'Wrong Answer',
		'sign': 'fa fa-fw fa-times',
		'color': '#ff4444'
	},
	7: {
		'name': 'Output Limit Exceeded',
		'sign': 'fa fa-fw fa-snowflake-o',
		'color': 'orange'
	},
	8: {
		'name': 'Time Limit Exceeded',
		'sign': 'fa fa-fw fa-clock-o',
		'color': 'orange'
	},
	9: {
		'name': 'Memory Limit Exceeded',
		'sign': 'fa fa-fw fa-microchip',
		'color': 'orange'
	},
	10: {
		'name': 'Runtime Error',
		'sign': 'fa fa-fw fa-exclamation',
		'color': 'purple'
	},
	11: {
		'name': 'Partially Accepted',
		'sign': 'fa fa-fw fa-adjust',
		'color': '#19d960'
	},
	12: {
		'name': 'Accepted',
		'sign': 'fa fa-fw fa-check',
		'color': '#1eee1e'
	},
	13: {
		'name': 'Skipped',
		'sign': 'fa fa-fw fa-forward',
		'color': '#999'
	},
}
