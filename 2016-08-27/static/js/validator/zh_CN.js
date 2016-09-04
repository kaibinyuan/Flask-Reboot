






<HTML>
<HEAD>
<!-- cmcccs|login_req||||||-->


<!--
<WISPAccessGatewayParam xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespace SchemaLocation="http://www.acmewisp.com/WISPAccessGatewayParam.xsd">
<Proxy>
<MessageType>110</MessageType>
<NextURL>http://cmccportal.ctclchina.com/guangdong/gis.php?Hotspot_operator=CMCC&Hotspot_location=guangdong&Nas_id=2135.0020.200.00&Nas_ip=211.136.215.35&User_ip=10.167.110.87&Client_type=wispr</NextURL>
<ResponseCode>200</ResponseCode>
<Delay>2</Delay>
</Proxy>
</WISPAccessGatewayParam>
-->
</HEAD>
<SCRIPT Language="JavaScript">
<!--
function autosubmit ()
{
   document.myForm.submit();
}
//-->
</SCRIPT>
<BODY onLoad="autosubmit()">
		<form name="loginform" action="http://221.179.9.21/bpss/jsp/do_login.jsp"  method="post">
			<input type="hidden" name="wlanacname"
				value="2135.0020.200.00" />
			<input type="hidden" name="wlanuserip"
				value="10.167.110.87" />
			<input type="hidden" name="actiontype" value="LOGIN" />
			<input type="hidden" name="wlanacssid" value="" />
			<input type="hidden" name="logonsessid" value="" />
			<input type="hidden" name="pwdtype" value="1" />
		</form>

<FORM NAME="myForm" action="index.jsp?testrand=1472637735646" method="post">
<INPUT TYPE="hidden" NAME="wlanuserip" value="10.167.110.87">
<INPUT TYPE="hidden" NAME="wlanacname" value="2135.0020.200.00">
<INPUT TYPE="hidden" NAME="wlanacip" value="211.136.215.35">
<INPUT TYPE="hidden" NAME="ssid" value="CMCC-FREE">

</FORM>
</BODY>
</HTML>
