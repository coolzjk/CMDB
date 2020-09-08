/**
 * Created by Jack on 2020/5/15.
 */
//dcroom
    function eachJZ(title, array) {
        var Jzhtml = '';
        var Type = '';
            for(var i=0;i<array.length;i++){
                for(var ii=0;ii<array[i].length;ii++){
                    if(array[i][ii]!=undefined){
                        for(var iii=0;iii<array[i][ii].length;iii++){
                            var position = array[i][ii].length-iii//可以算出当前正数的倒数，相当于从上至下倒成从下至上
                            if(array[i][ii][iii]==title){//当前机位为空的时候没有字典，值为一个单一的机柜编号，和传入的当前需要生成的机柜编号相等
                                Jzhtml += '<tr><td height="12px" width="2px" style="color: #b8c7ce">' + position+ '</td><td align="center" height="12px" valign="bottom"><div class="item_add" data-toggle="modal" data-target=".manual-add" onclick="ManualAdd(' + position + ',\''+array[i][ii][iii]+'\')"></div></td></tr>'
                            }else{//值如果不是机柜编号，就走下面逻辑
                                var models = array[i][ii][iii]['form']
                                if(array[i][ii][iii].TypeID=='1'){Box='box';Type='server';url='/detail/?nid=' + array[i][ii][iii].id + ''}else if(array[i][ii][iii].TypeID=='2'){Box='network';Type='switch';url='#'}else if(array[i][ii][iii].TypeID=='3'){Box='storage';Type='storage';url='#'}
                                if (array[i][ii][iii].cabinet_num == title) {
                                    var IpAdress=[];
                                    var management_ip=array[i][ii][iii].management_ip;
                                    for(var iiii=0;iiii<array[i][ii][iii].IpAdress.length;iiii++){
                                        IpAdress.push(array[i][ii][iii].IpAdress[iiii])
                                    }
                                    if (models == '1') {//鼠标悬浮后生把根据设备类型生成标签id为（box/network/storage+数据id号）的div标签，鼠标悬浮后把这个标签id号传给show函数去除display:none属性
                                        Jzhtml += ' <tr>'//鼠标放到设备上的注释标签,onmouseover及out属性传参给函数当前id及ip地址，show和hide函数修改id=box的div标签样式
                                            + '    <tr><td height="12px" width="2px" style="color: #b8c7ce">' + position + '</td><td class="jgtable" align="left" height="12px" valign="bottom" style="margin: 0px 0px 0px 0px;padding-top: 0px">'
                                            +'    <a href="' + url +'"><img src="/static/static/images/serverico/' + Type+array[i][ii][iii].device_status + '.gif" id="' + array[i][ii][iii].id + '" onmouseover="show(\'' + Box + '\',\''+ array[i][ii][iii].id +'\',\'' + IpAdress.toString() + '\')" onmouseout="hide(\'' + Box + ''+ array[i][ii][iii].id +'\')" style="vertical-align: bottom;" height="12" width="127"></a>'
                                            + '    <div id="'+Box+'' + array[i][ii][iii].id + '" style="border-style: outset; border-width: 1px 2px 2px 1px; display: none; position: absolute; width: 200px; text-align: left; background: none 0% 0% repeat scroll rgb(255, 255, 255);">'
                                            + '    <div>用途:'+ array[i][ii][iii].comment + '</div><div id="hostname">主机名:'+ array[i][ii][iii].hostname + '</div><div id="address"></div><div>资产编号:'+ array[i][ii][iii].AssetNumber + '</div><div>型号:'+ array[i][ii][iii].model + '</div><div>序列号:'+ array[i][ii][iii].sn + '</div>'
                                            + '    </div>'
                                            + '    </td>'
                                            + '  </tr>'
                                    } else if (models == '2'){
                                        Jzhtml += ' <tr>'//鼠标放到设备上的注释标签
                                            + '    <tr><td height="12px" width="2px" style="color: #b8c7ce">' + position + '</td><td class="jgtable" align="left" height="40px" valign="bottom">'
                                            +'    <a href="' + url +'"><img src="/static/static/images/serverico/' +Type+ array[i][ii][iii].device_status + '.gif" onmouseover="show(\'' + Box + '\',\''+ array[i][ii][iii].id +'\',\'' + IpAdress.toString() + '\',\''+ management_ip +'\')" onmouseout="hide(\'' + Box + ''+ array[i][ii][iii].id +'\')" style="vertical-align: bottom;" height="24" width="127"></a>'
                                            + '    <div id="'+Box+''  + array[i][ii][iii].id + '" style="border-style: outset; border-width: 1px 2px 2px 1px; display: none; position: absolute; width: 200px; text-align: left; background: none 0% 0% repeat scroll rgb(255, 255, 255);">'
                                            + '    <div>用途:'+ array[i][ii][iii].comment + '</div><div id="hostname">主机名:'+ array[i][ii][iii].hostname + '</div><div id="address"></div><div>资产编号:'+ array[i][ii][iii].AssetNumber + '</div><div>型号:'+ array[i][ii][iii].model + '</div><div>序列号:'+ array[i][ii][iii].sn + '</div>'
                                            + '    </div>'
                                            + '    </td>'
                                            + '  </tr>'
                                        iii=iii+1
                                    } else if (models == '4'){
                                        Jzhtml += ' <tr>'//鼠标放到设备上的注释标签
                                            + '    <tr><td height="12px" width="2px" style="color: #b8c7ce">' + position + '</td><td class="jgtable" align="left" height="80px" valign="bottom">'
                                            + '    <a href="' + url +'"><img src="/static/static/images/serverico/4u_' +Type+ array[i][ii][iii].device_status + '.gif" onmouseover="show(\'' + Box + '\',\''+ array[i][ii][iii].id +'\',\'' + IpAdress.toString() + '\',\''+ management_ip +'\')" onmouseout="hide(\'' + Box + ''+ array[i][ii][iii].id +'\')" style="vertical-align: bottom;" height="70" width="127"></a>'
                                            + '    <div id="'+Box+''  + array[i][ii][iii].id + '" style="border-style: outset; border-width: 1px 2px 2px 1px; display: none; position: absolute; width: 200px; text-align: left; background: none 0% 0% repeat scroll rgb(255, 255, 255);">'
                                            + '    <div>用途:'+ array[i][ii][iii].comment + '</div><div id="hostname">主机名:'+ array[i][ii][iii].hostname + '</div><div id="address"></div><div>资产编号:'+ array[i][ii][iii].AssetNumber + '</div><div>型号:'+ array[i][ii][iii].model + '</div><div>序列号:'+ array[i][ii][iii].sn + '</div>'
                                            + '    </div>'
                                            + '    </td>'
                                            + '  </tr>'
                                        iii=iii+3
                                    }else {
                                        Jzhtml += '<tr><td height="12px" width="2px" style="color: #b8c7ce">' + position + '</td><td align="center" height="12px" valign="bottom"><div class="item_add"  data-hasqtip="5" aria-describedby="qtip-2" data-toggle="popover" data-placement="right" data-trigger="hover"></div></td></tr>'
                                    }
                                }
                                }
                            }
                        }
                    }
                }return Jzhtml
        }
    function eachJG(title,array,w) {
        var cabinet_html = ''
                cabinet_html += '<td background="/static/static/images/serverico/jg.gif" bgcolor="#eeeeee" width=' + w + '>'
        + '  <table border="0" cellpadding="0" cellspacing="0" height="960px" width="100%">'
        + '    <thead>'
        + '      <tr>'
        + '      <p style="color:white">' + title + '</p>'
        + '        </tr>'
        + '     </thead>'
        + '     <tbody>'
        + '      <tr>'
                + eachJZ(title,array)
        + '        </tr>'
        + '     </tbody>'
        + '   </table>'
        + '</td>'
      return cabinet_html;
    }

    function htmlPanel(title,array) {
        var htmlPanel = ''
        w = 160
        htmlPanel += '<div align="center" style="width:' + w + 'px"></div>'
            + '<table class="jjtable" background="/static/static/images/serverico/jg.gif" style="float:left;" bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0" height="1050px" width=' + w + '>'
            + '  <tbody>'
            + '    <tr align="center" valign="top">' + eachJG(title,array,w) + '</tr>'
            + '  </tbody>'
            + '</table>';
        return htmlPanel
    }

  //根据机柜行数及列数计算宽度和高度创建racks_add
    var CabinetNum2 = $('.sep').text().split('*')
    var CabinetNum1 = $('.data')
    $('.racks_add').css({"width":CabinetNum2[0]*161,"height":"100%"})
    var PositionNum = 48 //每个机柜U位数
    var arr = new Array()
    function GetQueryString(name){//通过正则匹配获取url的nid参数值
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    }
    url = '/api/get_asset?nid='+GetQueryString('nid')
    $.getJSON(url,function (data) {//起初是想把getJson作为单独的函数，将取到的json串供之前写的逻辑调用，没有成功，之前的逻辑都写到这个getJSON这个函数下面了
        var emptyRack = JSON.parse(data['data']).EmptyRack//获取空机柜坐标的对象
        var data = JSON.parse(data['data']).data//这里已经从JSON串变成了对象,拿到key为data下的对象供循环获取value
        for (var i = 0; i < CabinetNum2[1]; i++) {//根据y轴的个数创建array，array内部的个数为x轴个数
            arr[i] = new Array(parseInt(CabinetNum2[0]))//取得一个y轴为多少，就有多少个key的，value为一个array的（个数为x轴数量）array
        }
        for (i = 0; i < data.length; i++) {
            var item = data[i].cabinet_order.split('*')//获取该机房全部服务器的x轴及y轴坐标
             var cabinet = data[i].cabinet_num
            item1 = parseInt(item[1]);//设备对应的X轴
            item2 = parseInt(item[0]);//设备对应的Y轴
            item3 = PositionNum-data[i].cabinet_pos;//机柜内U位
            if (arr[item1] && arr[item1][item2]) {//这里代表下面已经建过这个array结构有过数据，只要在相应的机柜内位置array里填充data[i]数据
                arr[item1][item2][item3] = data[i]
            } else {
                arr[item1][item2] = new Array(PositionNum).fill(cabinet);//空的array先生成一个array结构，值先都填充机柜编号
                arr[item1][item2][item3] = data[i];//再在本次循环对象的相应机柜内位置（通过item3换算，也就是array内相应的位置）写入data[i]数据
            }
        }

    var total = $('.sep').text().split('*');
    var y = []
    for (yy = 0; yy < total[1]; yy++) {
        y.push(yy)//拿到一个y轴长度的列表
    }
    for (yy in y) {
        for (x = 0; x < total[0]; x++) {//通过循环得到一个y对应的一个x
            var data = {'x': x, 'y': yy};//获得一个坐标的字典
            var add = "<div class='cell_add' data-x='" + data.x + "'/ data-y='" + data.y + "'/ data-toggle='modal' data-target='.bs-example-modal-sm' data-hasqtip='2' aria-describedby='qtip-2' data-toggle='popover' data-placement='right' data-trigger='hover' onclick='GiveOrder(this)'></div>"
            $('.racks_add').append(add)//根据坐标值创建全部空的div标签，到时候设备再通过自己的坐标值对号入座。
        }
    }
//以下开始对号入座,把获取的机柜编号放到对应坐标位置
    //这段逻辑开始构建动态机柜图
    var data = $('.data') //获取机柜信息
    var res = {}
    for (i = 0; i < data.length; i++) {//循环取机柜信息，获得具体的机柜数量。
        var num = data[i].innerHTML.split('/')//第一次提取，分开机柜位置和机柜编号
        var zuobiao = num[1].split('*')//对机柜坐标进行*号分割，取到x及y的值
        var reg = num[1];
        var datax = zuobiao[0]
        var datay = zuobiao[1]
        res.x = datax//把x及y的值存储城一个字典供下面根据坐标值进行匹配
        res.y = datay
        var res1 = $("div[data-x='" + res.x + "'][data-y='" + res.y + "']")//通过循环获得的机柜坐标匹配div标签
        if($.inArray(reg,emptyRack[0])!=-1){//判断这个机柜坐标是否为空机柜
            var arr1=new Array()
            arr1[0]=new Array()
            arr1[0][0]=new Array(PositionNum).fill(num[0])
            res1.removeClass('cell_add')
            res1.addClass('cell_exist')
            res1.removeAttr('data-toggle data-target')
            res1.append(htmlPanel(num[0], arr1))
        }else{//下面走的是本次循环reg没有在emptyRack[0]里，代表这个机柜有设备，走下面逻辑。
            res1.removeClass('cell_add')//对匹配到的标签进行修改，显示机柜编号。
            res1.addClass('cell_exist')
            res1.removeAttr('data-toggle data-target')
            res1.append(htmlPanel(num[0], arr))
        }
    }
})

    function ManualAdd(arg,arg1) {
        $("#cabinet").append("<option value="+arg1+"></option>")
        $("#position").append("<option value="+arg+"></option>")
    }

    function show(arg,arg1,IpAdress,management_ip) {//找到当前鼠标悬浮设备的弹出框标签（id=box+arg参数的标签），设置display属性
        var obj=arg+arg1
        if(arg=='box'){
            $("#"+obj+"").css('display','block')
            var IpAdress =IpAdress.split(',')
            for(var i=0;i<IpAdress.length;i++){
                $("#"+obj+" #address").append("<div class=\"IpAdress\">"+IpAdress[i]+"</div>")
                //$("#"+obj+"").append("<div class=\"ip\">"+ip[i]+"</div>")
            }
        }else if(arg=='storage'){
            $("#"+obj+"").css('display','block')
            $("#"+obj+"").find("#hostname").remove()
            $("#"+obj+" #address").append("<div class=\"IpAdress\">"+management_ip+"</div>")
        }else if(arg=='network'){
            $("#"+obj+"").css('display','block')
            $("#"+obj+"").find("#hostname").remove()
            $("#"+obj+" #address").append("<div class=\"IpAdress\">"+management_ip+"</div>")
        }

    }
    function hide(arg) {
        //var obj='box'+String(arg)
        $("#"+arg+"").css('display','none')
        $("#"+arg+"").find(".IpAdress").remove()
    }

   function GiveOrder(arg) {
        var xtime=$(arg).attr('data-x');
        var ytime=$(arg).attr('data-y');
        var location=xtime+'*'+ytime
        $('.cabinet_order').val(location)
    }

    for(i=1;i<43;i++){
        $('.carlist').append('<option selected = "selected" value="'+i+'">'+i+'</option>')
    }
    document.getElementById('sub').onclick=function () {
            $.ajax({
                url:'/dcroom/',
                type:'POST',
                data:$('#Data').serialize(),
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
    document.getElementById('sub_asset').onclick=function () {
        $.ajax({
            url: '/audit_asset/',
            type: 'POST',
            data: $('#SubAsset').serialize(),
            success: function (arg) {
                if (arg != 'ok') {
                    if (arg == 'no permission') {
                        $.message({
                            message: '失败，没有权限。',
                            duration: 1000,
                            type: 'error'
                        });
                        //setTimeout(function(){window.location.reload();},2000);
                    } else {
                        $.message({
                            message: '失败，请联系管理员。',
                            duration: 1000,
                            type: 'error'
                        });
                        //setTimeout(function(){window.location.reload();},2000);
                    }
                }
                else {
                    $.message({
                        message: '操作成功',
                        duration: 1000,
                        type: 'success'
                    });
                    setTimeout(function () {
                        window.location.reload();
                    }, 2000);
                }
            },
        })
    }