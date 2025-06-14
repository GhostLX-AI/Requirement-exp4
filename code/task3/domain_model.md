===== 用例图 =====
```json
{
  "actors": ["学生", "教师", "管理员"],
  "usecases": [
    {
      "name": "查看可选课程",
      "description": "学生可以查看当前可供选择的课程列表。",
      "actor": "学生"
    },
    {
      "name": "选课",
      "description": "学生选择要修的课程。",
      "actor": "学生",
      "include": ["审核选课冲突"],
      "extend": ["课程容量限制"]
    },
    {
      "name": "退选",
      "description": "学生可以退选已经选择的课程。",
      "actor": "学生"
    },
    {
      "name": "查看已选课程",
      "description": "学生查看自己已经选定的课程列表。",
      "actor": "学生"
    },
    {
      "name": "查看成绩",
      "description": "学生查看自己的课程成绩。",
      "actor": "学生"
    },
    {
      "name": "管理课程",
      "description": "教师可以添加、修改或删除课程信息。",
      "actor": "教师"
    },
    {
      "name": "录入成绩",
      "description": "教师录入课程成绩。",
      "actor": "教师"
    },
    {
      "name": "查看选课学生",
      "description": "教师查看选课学生名单。",
      "actor": "教师"
    },
    {
      "name": "管理用户",
      "description": "管理员管理系统内的用户信息，包括学生、教师和管理员。",
      "actor": "管理员"
    },
    {
      "name": "管理系统参数",
      "description": "管理员管理系统配置和参数。",
      "actor": "管理员"
    },
    {
      "name": "审核选课冲突",
      "description": "系统检测课程之间的时间冲突。",
      "actor": "系统"
    }
  ]
}
```

===== 系统顺序图 =====

顺序图 1:
```json
{
  "for_usecase": "查看可选课程",
  "messages": [
    {
      "sender": "学生",
      "receiver": "系统",
      "message": "请求查看可选课程列表",
      "parameters": null
    },
    {
      "sender": "系统",
      "receiver": "学生",
      "message": "提供可选课程列表",
      "parameters": ["课程列表"]
    }
  ]
}
```

顺序图 2:
```json
{
  "for_usecase": "选课",
  "messages": [
    {
      "sender": "学生",
      "receiver": "系统",
      "message": {
        "name": "请求选课",
        "parameters": {
          "课程ID": "courseId",
          "学生ID": "studentId"
        }
      }
    },
    {
      "sender": "系统",
      "receiver": "系统",
      "message": {
        "name": "审核选课冲突",
        "parameters": {
          "学生ID": "studentId",
          "课程ID": "courseId"
        }
      }
    },
    {
      "sender": "系统",
      "receiver": "系统",
      "message": {
        "name": "检查课程容量限制",
        "parameters": {
          "课程ID": "courseId"
        }
      }
    },
    {
      "sender": "系统",
      "receiver": "学生",
      "message": {
        "name": "选课结果",
        "parameters": {
          "课程ID": "courseId",
          "状态": "成功/失败",
          "原因": "reason"
        }
      }
    }
  ]
}
```

顺序图 3:
```json
{
  "for_usecase": "退选",
  "messages": [
    {
      "sender": "学生",
      "receiver": "系统",
      "name": "请求退选",
      "parameters": {
        "课程ID": "courseId"
      }
    },
    {
      "sender": "系统",
      "receiver": "数据库",
      "name": "检查课程状态",
      "parameters": {
        "课程ID": "courseId",
        "学生ID": "studentId"
      }
    },
    {
      "sender": "数据库",
      "receiver": "系统",
      "name": "返回课程状态",
      "parameters": {
        "状态": "status"
      }
    },
    {
      "sender": "系统",
      "receiver": "数据库",
      "name": "更新已选课程",
      "parameters": {
        "课程ID": "courseId",
        "学生ID": "studentId"
      }
    },
    {
      "sender": "数据库",
      "receiver": "系统",
      "name": "确认更新",
      "parameters": {
        "结果": "success"
      }
    },
    {
      "sender": "系统",
      "receiver": "学生",
      "name": "确认退选结果",
      "parameters": {
        "结果": "success",
        "课程名称": "courseName"
      }
    }
  ]
}
```

===== 概念类图 =====
```json
{
  "classes": [
    {
      "name": "学生",
      "attributes": ["学生ID", "姓名", "邮箱", "已选课程"],
      "methods": ["查看可选课程", "选课", "退选", "查看已选课程", "查看成绩"]
    },
    {
      "name": "课程",
      "attributes": ["课程ID", "课程名称", "描述", "容量", "已选人数"],
      "methods": ["添加课程", "修改课程", "删除课程", "检查冲突", "检查容量限制"]
    },
    {
      "name": "教师",
      "attributes": ["教师ID", "姓名", "邮箱", "课程列表"],
      "methods": ["管理课程", "录入成绩", "查看选课学生"]
    },
    {
      "name": "管理员",
      "attributes": ["管理员ID", "姓名", "邮箱"],
      "methods": ["管理用户", "管理系统参数"]
    },
    {
      "name": "系统",
      "attributes": [],
      "methods": ["审核选课冲突"]
    }
  ],
  "relationships": [
    {
      "type": "association",
      "from": "学生",
      "to": "课程",
      "name": "选修"
    },
    {
      "type": "association",
      "from": "教师",
      "to": "课程",
      "name": "教授"
    },
    {
      "type": "aggregation",
      "from": "课程",
      "to": "学生",
      "name": "选择课程"
    },
    {
      "type": "association",
      "from": "管理员",
      "to": "学生",
      "name": "管理"
    },
    {
      "type": "association",
      "from": "管理员",
      "to": "教师",
      "name": "管理"
    },
    {
      "type": "association",
      "from": "管理员",
      "to": "系统",
      "name": "配置系统"
    }
  ]
}
```

===== OCL合约 =====
```json
{
  "constraints": [
    {
      "context": "学生",
      "type": "invariant",
      "expression": "self.邮箱 <> null and self.邮箱.matches('^\\S+@\\S+\\.\\S+$')"
    },
    {
      "context": "学生::选课(课程)",
      "type": "precondition",
      "expression": "课程.检查容量限制() and not courses->includes(课程)"
    },
    {
      "context": "学生::选课(课程)",
      "type": "postcondition",
      "expression": "已选课程->includes(课程) and 课程.已选人数 = 课程.已选人数@pre + 1"
    },
    {
      "context": "学生::退选(课程)",
      "type": "precondition",
      "expression": "已选课程->includes(课程)"
    },
    {
      "context": "学生::退选(课程)",
      "type": "postcondition",
      "expression": "not 已选课程->includes(课程) and 课程.已选人数 = 课程.已选人数@pre - 1"
    },
    {
      "context": "课程",
      "type": "invariant",
      "expression": "容量 > 0 and 已选人数 <= 容量"
    },
    {
      "context": "课程::检查容量限制()",
      "type": "postcondition",
      "expression": "result = (已选人数 < 容量)"
    },
    {
      "context": "教师",
      "type": "invariant",
      "expression": "self.邮箱 <> null and self.邮箱.matches('^\\S+@\\S+\\.\\S+$')"
    },
    {
      "context": "管理员",
      "type": "invariant",
      "expression": "self.邮箱 <> null and self.邮箱.matches('^\\S+@\\S+\\.\\S+$')"
    }
  ]
}
```
