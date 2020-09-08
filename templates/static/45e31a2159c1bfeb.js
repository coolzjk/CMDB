/**
 * Created by Jack on 2020/5/15.
 */
//asset
    document.getElementById('add').onclick = function () {//点击加号后的逻辑'#SearchField'下拉框取消隐藏
        $('#SearchField').append("<option value='AssetType'>设备类型</option><option value='AssetStatus'>设备状态</option>")
        $('#SearchField').attr('style',"width: 110px;")//把这个下拉框取消隐藏即可显示第一个下拉框：操作类型
        $('#AssetType').attr('style',"width: 110px;")//把forms里给到两个下拉框一个先取消隐藏
        $('#AssetType').removeAttr("disabled")
        $('#AssetStatus').attr({'disabled':'disabled'})
        $(this).attr('style','display:none')//隐藏加号
        $('#del').removeAttr('style')//显示减号
    };

    document.getElementById('del').onclick=function () {//点击减号后的逻辑
        $(this).attr('style','display:none')
        $('#SearchField').attr('style',"display:none")
        $('#AssetType').attr('style',"display:none")
        $('#add').removeAttr('style')
        $('#SearchField option').remove()
    }
    document.getElementById('SearchField').onchange = function () {//高级搜索项第一个下拉框发送变化后的逻辑
        var selected = $(this).find("option:selected").val()//找到哪个option被选中并拿到value
        $('#'+selected).siblings("#AssetType ,#AssetStatus").attr('style','display:none')
        $('#'+selected).siblings("#AssetType ,#AssetStatus").attr({'disabled':'disabled'})
        $('#'+selected).attr('style',"width: 110px;").removeAttr("disabled")
    }

//模态对话框
    var nid = null
    $('.removee').bind('click',function () {
        nid = $(this).parent().siblings().find('#nid').val()
        var thiss = $(this)
        document.getElementById('confirm').innerHTML=''
        $('#confirm').append('确认'+thiss.attr("control")+'？')
    })
    document.getElementById('DelAsset').onclick=function () {
        $.ajax({
            url:'/asset/',
            type:'POST',
            data:{'RemoveAsset':'True','nid':nid},
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

