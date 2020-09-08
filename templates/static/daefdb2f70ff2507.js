/**
 * Created by Jack on 2020/5/15.
 */
//datacenter
    $('#select').children().find('.RackNumber').each(function () {
        var x= $(this).html().split('*')
        var num="行数：<div class='text xy' style='display: inline'>"+x[1]+"</div>列数：<div class='text xy' style='display: inline'>"+x[0]+"</div>";
        $(this).parent().append(num)
    })

    document.getElementById('subLocation').onclick =function () {
        $.ajax({
            url:'/location/',
            type:'POST',
            data:$('#IdcData').serialize(),
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
    $('#select').find('.edit').click(function () {
        if($(this).is('.edit')){
            $(this).parent().parent().children().each(function () {
                $(this).find('.xy').each(function () {
                    var orgin_value = $(this).text();
                    var tmp = "<input style='width:15px' type=text value='" + orgin_value + "' />";
                    $(this).html(tmp);
                })

                if ($(this).is('.text')) {
                    var orgin_value = $(this).text();
                    var tmp = "<input type=text value='" + orgin_value + "' />";
                    $(this).html(tmp);
                } else {
                    var obj_edit = $(this).find('.edit');
                    obj_edit.text('保存');
                    obj_edit.removeClass("btn-primary edit");
                    obj_edit.addClass('btn-warning editing');
                }
            })
        }else{
            $(this).parent().parent().children().each(function () {
                $(this).find('.xy').each(function () {
                    var orgin_value = $(this).find("input").val();
                    $(this).html(orgin_value);
                })
                if ($(this).is('.text')) {
                    var orgin_value = $(this).find("input").val();
                    $(this).html(orgin_value);
                    var status = $(this).parent().find("#status");
                    status.html("update");
                }else{
                    var obj_editing = $(this).find('.editing');
                    obj_editing.text('编辑');
                    obj_editing.removeClass('btn-warning editing');
                    obj_editing.addClass("btn-primary edit");
                }
            })
            var name = $(this).parent().parent().find('#name').html();
            var floor = $(this).parent().parent().find('#floor').html();
            var address = $(this).parent().parent().find('#address').html();
            var id = $(this).parent().parent().find('#id_num').html();
            var status = $(this).parent().parent().find('#status').html();
            var xy = []
            $(this).parent().parent().find('.xy').each(function () {
                xy.push($(this).text())
            });
            $.ajax({
                url:'/location/',
                type:'POST',
                data:{'name':name,'floor':floor,'id':id,'status':status,'address':address,'XY':xy,},
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
    })