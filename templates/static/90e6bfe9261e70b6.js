/**
 * Created by Jack on 2020/5/15.
 */
//audit_asset
$('.approve').bind('click',function () {
       $("#idc option").remove();$("#cabinet option").remove();
        var approve_host = $(this).parent().parent().children().find('#hostname').val();
        $("#approve_hostname").append('<option value="'+approve_host+'"></option>');
        url = "/api/get_idc"
        $.getJSON(url,function(data) {
            data = data['data']

            for(idc in data) {//动态添加机柜编号到id="idc"的select标签内
                $("#idc").append('<option value="' + idc + '">' + idc + '</option>')
            }
            selected=$("#idc option").html()//根据idc名设置初始机柜栏目
            for(i=0;i<data[selected].length;i++){
                $("#cabinet").append('<option value="' + data[selected][i] + '">' + data[selected][i] + '</option>')
            }
            //根据选择机房名称动态调整机柜编号
            document.getElementById('idc').onchange=function () {
                $("#cabinet option").remove()
                var rack=data[this.options[this.selectedIndex].innerHTML];//获取onchange选择的该option的值
                for(var i=0;i<rack.length;i++) {
                    var ele = document.createElement("option");
                    ele.innerHTML = rack[i];//通过api查询机柜编号，key的值为当前选择的机房名字(innerHTML)
                    document.getElementById('cabinet').appendChild(ele);
                }
            }
        })
    })
//拒绝审核后的逻辑
    var operator = null
    var hostname = null
    var thiss = $(this)
        $('.remove,.reject').bind('click',function () {
        nid = $(this).parent().siblings().find('#nid').val();
        operator = $(this).attr("class")
        hostname = $(this).parent().parent().children().find('#hostname').val();
        document.getElementById('confirm').innerHTML=''//先清除再添加，否则上一个添加的确认不会去除
        $('#confirm').append('确认'+$(this).attr("control")+'？')//前端拒绝按钮标签自定义一个control属性用于确认卡动态显示
    })
    document.getElementById('AuditDelete').onclick=function () {
        if(operator.indexOf("reject")==-1){
            operator = 'remove'
        }else if(operator.indexOf("remove")==-1) {
            operator = 'reject'
        }
        thiss.parent().parent().css("background-color", "#e5e5e5")
        $.ajax({//这里拒绝了后还要往后端传数据是为了能在前端显示这条数据时候置灰
            url:'/audit_asset/',
            type:'POST',
            data:{'operator':operator,'hostname':hostname},
            success:function (arg) {
                if (arg != 'ok'){
                    if (arg == 'no permission'){
                        $.message({
                            message:'失败，没有权限。',
                            duration:1000,
                            type:'error'
                        });
                    //setTimeout(function(){window.location.reload();},2000);
                    }else {
                        $.message({
                            message:'失败，请联系管理员。',
                            duration:1000,
                            type:'error'
                        });
                    //setTimeout(function(){window.location.reload();},2000);
                    }
                }
                else {
                       $.message({
                            message:'操作成功',
                            duration:1000,
                            type:'success'
                        });
                    setTimeout(function(){window.location.reload();},2000);
                }
            },
        })
    }
    document.getElementById('sub').onclick =function (){//同意审核后的逻辑

        $.ajax({
            url:'/audit_asset/',
            type:'POST',
            data:$('#asset').serialize(),
            success:function (arg) {
                if (arg != 'ok'){
                    if (arg == 'no permission'){
                        $.message({
                            message:'失败，没有权限。',
                            duration:1000,
                            type:'error'
                        });
                    //setTimeout(function(){window.location.reload();},2000);
                    }else {
                        $.message({
                            message:'失败，请联系管理员。',
                            duration:1000,
                            type:'error'
                        });
                    //setTimeout(function(){window.location.reload();},2000);
                    }
                }
                else {
                       $.message({
                            message:'操作成功',
                            duration:1000,
                            type:'success'
                        });
                    setTimeout(function(){window.location.reload();},2000);
                }
            },
        })
    }

