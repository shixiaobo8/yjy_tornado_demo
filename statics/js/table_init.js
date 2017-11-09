/**
     * 提交json数据的post请求
     * @author laixm
     */
    $.postJSON = function(url,data,callback){
        $.ajax({
            url:url,
            type:"post",
            contentType:"application/json",
            dataType:"json",
            data:data,
            timeout:60000,
            success:function(msg){
                callback(msg);
            },
            error:function(xhr,textstatus,thrown){

            }
        });
    };

    /**
     * 修改数据的ajax-put请求
     * @author laixm
     */
    $.putJSON = function(url,data,callback){
        $.ajax({
            url:url,
            type:"put",
            contentType:"application/json",
            dataType:"json",
            data:data,
            timeout:20000,
            success:function(msg){
                callback(msg);
            },
            error:function(xhr,textstatus,thrown){

            }
        });
    };
    /**
     * 删除数据的ajax-delete请求
     * @author laixm
     */
    $.deleteJSON = function(url,data,callback){
        $.ajax({
            url:url,
            type:"delete",
            contentType:"application/json",
            dataType:"json",
            data:data,
            success:function(msg){
                callback(msg);
            },
            error:function(xhr,textstatus,thrown){

            }
        });
    };

/**
     * 提交json数据的post请求
     * @author laixm
     */
    $.postJSON = function(url,data,callback){
        $.ajax({
            url:url,
            type:"post",
            contentType:"application/json",
            dataType:"json",
            data:data,
            timeout:60000,
            success:function(msg){
                callback(msg);
            },
            error:function(xhr,textstatus,thrown){

            }
        });
    };

$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();

    //2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();

});

$table = $("#interFields");
$remove = $('#remove');
var baseUrl = '/';

var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#interFields').bootstrapTable({
            url: '/tabletest',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'key',
                title: '字段名称',
                align: 'center',
                editable: {
                       type: 'text',
                       validate: function (value) {
                           if ($.trim(value) == '') {
                               return 'key不能为空!';
                           }
                       }
                   }
            }, {
                field: 'value',
                title: '字段值',
                align: 'center',
                editable: {
                       type: 'text',
                       validate: function (value) {
                           if ($.trim(value) == '') {
                               return 'value不能为空!';
                           }
                       }
                   }
            }, {
                   field: 'operation',
                   title: '操作',
                   width: 100,
                   formatter: function (value, row, index) {
                       var s = '<a class = "save" href="javascript:void(0)">保存</a>';
                       var d = '<a class = "remove" href="javascript:void(0)">删除</a>';
                       return s + ' ' + d;
                   },
                   events: 'operateEvents'
               }]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            departmentname: $("#txt_search_departmentname").val(),
            statu: $("#txt_search_statu").val()
        };
        return temp;
    };
    return oTableInit;
};


var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
    };

    return oInit;
};
// 行内编辑保存删除
 window.operateEvents = {
               'click .save': function (e, value, row, index) {
                   $.ajax({
                       type: "post",
                       data: row,
                       url: '/interFeildSave',
                       success: function (data) {
                           alert('修改成功');
                       }
                   });
               },
               'click .remove': function (e, value, row, index) {
                   $.ajax({
                       type: "post",
                       data: row,
                       url: '/interFeildDelete',
                       success: function (data) {
                           alert('删除成功');
                           $('#table').bootstrapTable('remove', {
                               field: 'Id',
                               values: [row.Id]
                           });
                       }
                   });
               }
           };

// 行外新增加
$(document).ready(function(){
    //initvalueInpect();
    //表格初始化
    var oTable = new TableInit();
    oTable.Init();
    //查询
   /* $("#queryBtn").click(function(){
        $table.bootstrapTable('destroy');//表格销毁
        oTable.Init()
    });*/
    $("#add").click(function(){
        var key = $("#keyInp").val();
        var value =$("#valueInp").val();
            value = value=="*"?"":value;
        var  $remind = $(".remind");
        if($(this).find("i").hasClass("adding")){//提交新建数据
            if(key==''){
                $remind.html(' <i class="icon icon-info-sign">字段名不能为空!</i>');
                return;
            }
            if(/(^\s+)|(\s+$)/g.test(name)){
                $remind.html(' <i class="icon icon-info-sign">字段名不能输入空格!</i>');
                return;
            }
            if(key.length>20){
                $remind.html(' <i class="icon icon-info-sign">字段名不能超过20个字符!</i>');
                return;
            }
  //博主封装的ajax方法，详见我另外一篇博客   http://blog.csdn.net/u010543785/article/details/52366495
  $.postJSON(baseUrl+"interFeildAdd",'{"key":"'+key+'","value":"'+value+'"}',function(data){
                if(data>0){
                    $("#valueInp").css("display","none");
                    $("#valueInp").val("*");
                    $("#keyInp").css("display","none");
                    $("#keyInp").val("");
                    $("#cancel").css("display", "none");
                    $remind.html('');
                    $("#add").html('<i class="glyphicon glyphicon-plus"></i> 新建');
                    $table.bootstrapTable('destroy');//表格销毁
                    oTable.Init();
                    $.gritter.add({
                        title: '提示',
                        text: '新建接口字段成功!',
                        sticky: false,
                        time: 2500
                    });
                    //initvalueInpect();
                }else{
                    alert("新建接口字段失败，请联系技术人员!");
                }
            })
        }else {
            $("#keyInp").css("display", "block");
            $("#valueInp").css("display", "block");
            $("#cancel").css("display", "inline-block");
            $("#keyInp").focus();
            $("#add").html('<i class="glyphicon glyphicon-ok-circle adding"></i> 确认');
        }
    });
});
$("#cancel").click(function(){
    $("#valueInp").css("display","none");
    $("#valueInp").val("*");
    $("#keyInp").css("display","none");
    $("#keyInp").val("");
    $("#add").html('<i class="glyphicon glyphicon-plus"></i> 新建');
    $(".remind").html('');
    $(this).css("display","none");
});


//批量删除操作
$table.on('check.bs.table uncheck.bs.table ' +
    'check-all.bs.table uncheck-all.bs.table', function () {
    $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
    // save your data, here just save the current page
    selections = getIdSelections();
    // push or splice the selections if you want to save all data selections
});
$table.on('expand-row.bs.table', function (e, index, row, $detail) {
    if (index % 2 == 1) {
        $detail.html('Loading from ajax request...');
        $.get('LICENSE', function (res) {
            $detail.html(res.replace(/\n/g, '<br>'));
        });
    }
});
$remove.click(function () {
    var ids = getIdSelections();
    //博主封装的ajax方法，详见我另外一篇博客   http://blog.csdn.net/u010543785/article/details/52366495
    $.putJSON(baseUrl+"department/deletes","["+ids.toString()+"]",function(data){
        if(data>0){
            $table.bootstrapTable('remove', {
                field: 'id',
                values: ids
            });
            $.gritter.add({
                title: '提示',
                text: '删除接口字段成功!',
                sticky: false,
                time: 2500
            });
        }else{
            alert("删除失败，请联系技术人员!");
        }
    });
    $remove.prop('disabled', true);
});
function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.id
    });
}