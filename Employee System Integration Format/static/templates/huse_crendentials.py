

def huse_credentials_template(subject: str, employee_name: str, username: str, password: str, security_question: str, security_answer: str, preview_text: str = "Account login credentials"):
    # template = """<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head>
    #     <!--[if gte mso 15]>
    #     <xml>
    #     <o:OfficeDocumentSettings>
    #     <o:AllowPNG/>
    #     <o:PixelsPerInch>96</o:PixelsPerInch>
    #     </o:OfficeDocumentSettings>
    #     </xml>
    #     <![endif]-->
    #     <meta charset="UTF-8"/>
    #     <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    #     <meta name="viewport" content="width=device-width, initial-scale=1"/>
    #     <title>SUBJECT_PLACEHOLDER</title>
    #     <link rel="preconnect" href="https://fonts.googleapis.com"/>
    #     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>
    #     <!--[if !mso]><!--><link rel="stylesheet" type="text/css" id="newGoogleFontsStatic" href="https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i,900,900i"/><!--<![endif]--><style>img{-ms-interpolation-mode:bicubic;}
    #     table, td{mso-table-lspace:0pt;mso-table-rspace:0pt;}
    #     .mceStandardButton, .mceStandardButton td, .mceStandardButton td a{mso-hide:all!important;}
    #     p, a, li, td, blockquote{mso-line-height-rule:exactly;}
    #     p, a, li, td, body, table, blockquote{-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%;}
    #     .mcnPreviewText{display:none!important;}
    #     .bodyCell{margin:0 auto;padding:0;width:100%;}
    #     .ExternalClass, .ExternalClass p, .ExternalClass td, .ExternalClass div, .ExternalClass span, .ExternalClass font{line-height:100%;}
    #     .ReadMsgBody, .ExternalClass{width:100%;}
    #     a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important;}
    #     body{height:100%;margin:0;padding:0;width:100%;background:#ffffff;}
    #     p{margin:0;padding:0;}
    #     table{border-collapse:collapse;}
    #     td, p, a{word-break:break-word;}
    #     h1, h2, h3, h4, h5, h6{display:block;margin:0;padding:0;}
    #     img, a img{border:0;height:auto;outline:none;text-decoration:none;}
    #     a[href^="tel"], a[href^="sms"]{color:inherit;cursor:default;text-decoration:none;}
    #     .mceColumn .mceButtonLink,
    #                     .mceColumn-1 .mceButtonLink, 
    #                     .mceColumn-2 .mceButtonLink, 
    #                     .mceColumn-3 .mceButtonLink,
    #                     .mceColumn-4 .mceButtonLink{min-width:30px;}
    #     div[contenteditable="true"]{outline:0;}
    #     .mceImageBorder{display:inline-block;}
    #     .mceImageBorder img{border:0!important;}
    #     body, #bodyTable{background-color:rgb(244, 244, 244);}
    #     .mceText, .mcnTextContent, .mceLabel{font-family:"Helvetica Neue", Helvetica, Arial, Verdana, sans-serif;}
    #     .mceText, .mcnTextContent, .mceLabel{color:rgb(0, 0, 0);}
    #     .mceText h1, .mceText p, .mceText label, .mceText input{margin-bottom:0;}
    #     .mceSpacing-12 .mceInput + .mceErrorMessage{margin-top:-6px;}
    #     .mceSpacing-24 .mceInput + .mceErrorMessage{margin-top:-12px;}
    #     .mceInput{background-color:transparent;border:2px solid rgb(208, 208, 208);width:60%;color:rgb(77, 77, 77);display:block;}
    #     .mceInput[type="radio"], .mceInput[type="checkbox"]{float:left;margin-right:12px;display:inline;width:auto!important;}
    #     .mceLabel > .mceInput{margin-bottom:0;margin-top:2px;}
    #     .mceLabel{display:block;}
    #     .mceText p, .mcnTextContent p{color:rgb(0, 0, 0);font-family:"Helvetica Neue", Helvetica, Arial, Verdana, sans-serif;font-size:16px;font-weight:normal;line-height:1.5;mso-line-height-alt:150%;text-align:left;letter-spacing:0;direction:ltr;margin:0;}
    #     .mceText h1, .mcnTextContent h1{color:rgb(0, 0, 0);font-family:"Helvetica Neue", Helvetica, Arial, Verdana, sans-serif;font-size:31px;font-weight:bold;line-height:1.5;mso-line-height-alt:150%;text-align:left;letter-spacing:0;direction:ltr;}
    #     .mceText a, .mcnTextContent a{color:rgb(0, 0, 0);font-style:normal;font-weight:normal;text-decoration:underline;direction:ltr;}
    #     p.mcePastedContent, h1.mcePastedContent, h2.mcePastedContent, h3.mcePastedContent, h4.mcePastedContent{text-align:left;}
    #     #d13 p, #d13 h1, #d13 h2, #d13 h3, #d13 h4, #d13 ul{text-align:center;}
    #     @media only screen and (max-width: 480px) {
    #     body, table, td, p, a, li, blockquote{-webkit-text-size-adjust:none!important;}
    #     body{width:100%!important;min-width:100%!important;}
    #     body.mobile-native{-webkit-user-select:none;user-select:none;transition:transform 0.2s ease-in;transform-origin:top center;}
    #     colgroup{display:none;}
    #     .mceLogo img, .mceImage img, .mceSocialFollowIcon img{height:auto!important;}
    #     .mceWidthContainer{max-width:660px!important;}
    #     .mceColumn, .mceColumn-2{display:block!important;width:100%!important;}
    #     .mceColumn-forceSpan{display:table-cell!important;width:auto!important;}
    #     .mceColumn-forceSpan .mceButton a{min-width:0!important;}
    #     .mceReverseStack{display:table;width:100%;}
    #     .mceColumn-1{display:table-footer-group;width:100%!important;}
    #     .mceColumn-3{display:table-header-group;width:100%!important;}
    #     .mceColumn-4{display:table-caption;width:100%!important;}
    #     .mceKeepColumns .mceButtonLink{min-width:0;}
    #     .mceBlockContainer, .mceSpacing-24{padding-right:16px!important;padding-left:16px!important;}
    #     .mceBlockContainerE2E{padding-right:0;padding-left:0;}
    #     .mceImage, .mceLogo{width:100%!important;height:auto!important;}
    #     .mceText img{max-width:100%!important;}
    #     .mceFooterSection .mceText, .mceFooterSection .mceText p{font-size:16px!important;line-height:140%!important;}
    #     .mceText p{margin:0;font-size:16px!important;line-height:1.5!important;mso-line-height-alt:150%;}
    #     .mceText h1{font-size:31px!important;line-height:1.5!important;mso-line-height-alt:150%;}
    #     .bodyCell{padding-left:16px!important;padding-right:16px!important;}
    #     .mceDividerContainer{width:100%!important;}
    #     #b3{padding:0 48px!important;}
    #     #b3 table{margin-right:auto!important;float:none!important;}
    #     #b7 .mceTextBlockContainer{padding:12px 24px!important;}
    #     #gutterContainerId-7, #gutterContainerId-13, #gutterContainerId-19{padding:0!important;}
    #     #b13 .mceTextBlockContainer{padding:12px 16px!important;}
    #     #b19 .mceTextBlockContainer{padding:0 24px 18px!important;}
    #     #b25 .mceDividerBlock{border-top-width:1px!important;}
    #     #b25{padding:14px 24px 12px!important;}
    #     }
    #     @media only screen and (max-width: 640px) {
    #     .mceClusterLayout td{padding:4px!important;}
    #     }</style></head>
    #     <body>
    #     <!--*|IF:MC_PREVIEW_TEXT|*-->
    #     <!--[if !gte mso 9]><!----><span class="mcnPreviewText" style="display:none; font-size:0px; line-height:0px; max-height:0px; max-width:0px; opacity:0; overflow:hidden; visibility:hidden; mso-hide:all;">PREVIEW_TEXT_PLACEHOLDER</span><!--<![endif]-->
    #     <!--*|END:IF|*-->
    #     <div style="display: none; max-height: 0px; overflow: hidden;">͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌    ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­</div><!--MCE_TRACKING_PIXEL-->
    #     <center>
    #     <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="background-color: rgb(244, 244, 244);">
    #     <tbody><tr>
    #     <td class="bodyCell" align="center" valign="top">
    #     <table id="root" border="0" cellpadding="0" cellspacing="0" width="100%"><tbody data-block-id="5" class="mceWrapper"><tr><td style="background-color:transparent" valign="top" align="center" class="mceSectionHeader"><!--[if (gte mso 9)|(IE)]><table align="center" border="0" cellspacing="0" cellpadding="0" width="660" style="width:660px;"><tr><td><![endif]--><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:660px" role="presentation"><tbody><tr><td style="background-color:#ffffff" valign="top" class="mceWrapperInner"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="4"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" id="mceColumnId--7" data-block-id="-7" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="background-color:#ffffff;padding-top:0;padding-bottom:0;padding-right:48px;padding-left:48px;border:0;border-radius:0" valign="top" class="mceImageBlockContainer" align="left" id="b3"><div><!--[if !mso]><!--></div><a href="http://www.huse.ai" style="display:block" target="_blank" data-block-id="3"><table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate;margin:0;vertical-align:top;max-width:100%;width:100%;height:auto" role="presentation" data-testid="image-3"><tbody><tr><td style="border:0;border-radius:0;margin:0" valign="top"><img alt="" src="https://mcusercontent.com/360a033fa9b35032b8dab5b54/images/cc58c666-7ac9-0a72-5a57-2e672cab5778.png" width="564" height="auto" style="display:block;max-width:100%;height:auto;border-radius:0" class="imageDropZone mceLogo"/></td></tr></tbody></table></a><div><!--<![endif]--></div><div>
    #     <!--[if mso]>
    #     <a href="http://www.huse.ai"><span class="mceImageBorder" style="border:0;border-width:2px;vertical-align:top;margin:0"><img role="presentation" class="imageDropZone mceLogo" src="https://mcusercontent.com/360a033fa9b35032b8dab5b54/images/cc58c666-7ac9-0a72-5a57-2e672cab5778.png" alt="" width="564" height="auto" style="display:block;max-width:564px;width:564px;height:auto"/></span></a>
    #     <![endif]-->
    #     </div></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></tbody><tbody data-block-id="11" class="mceWrapper"><tr><td style="background-color:transparent" valign="top" align="center" class="mceSectionBody"><!--[if (gte mso 9)|(IE)]><table align="center" border="0" cellspacing="0" cellpadding="0" width="660" style="width:660px;"><tr><td><![endif]--><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:660px" role="presentation"><tbody><tr><td style="background-color:#ffffff" valign="top" class="mceWrapperInner"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="10"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" id="mceColumnId--8" data-block-id="-8" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" class="mceGutterContainer" id="gutterContainerId-7"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" id="b7"><table width="100%" style="border:0;background-color:transparent;border-radius:0;border-collapse:separate"><tbody><tr><td style="padding-left:24px;padding-right:24px;padding-top:12px;padding-bottom:12px" class="mceTextBlockContainer"><div data-block-id="7" class="mceText" id="d7" style="width:100%"><h1 class="last-child"><span style="font-size: 28px"><span style="font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif">Hey EMPLOYEE_NAME_PLACEHOLDER,</span></span></h1></div></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" class="mceGutterContainer" id="gutterContainerId-19"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" id="b19"><table width="100%" style="border:0;background-color:transparent;border-radius:0;border-collapse:separate"><tbody><tr><td style="padding-left:24px;padding-right:24px;padding-top:0;padding-bottom:18px" class="mceTextBlockContainer"><div data-block-id="19" class="mceText" id="d19" style="width:100%"><h1 class="mcePastedContent last-child" style="line-height: 1; mso-line-height-alt: 100%;"><span style="font-size: 13px"><span style="font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif"><span style="font-weight:normal;">Your HÜSE account has been successfully created. Please find your secure login credentials below.</span></span></span></h1></div></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td style="border:0;border-radius:0" valign="top" id="b24"><div data-block-id="24" class="mceCode"><!-- Center wrapper -->
    #     <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="100%" style="margin:0;padding:0;">
    #     <tbody><tr>
    #     <td align="center" style="margin:0;padding:0;">
    #     <!-- Outer card -->
    #     <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="560" style="width:560px; max-width:560px; font-family:Roboto, Arial, sans-serif; color:#111; background:#ffffff; border:1px solid #e6e6e6;">
    #     <tbody><tr>
    #     <td style="padding:24px;">
    #     <!-- LOGIN -->
    #     <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="border:1px solid #ededed;">
    #     <tbody><tr>
    #     <td style="padding:16px;">
    #     <div style="font-size:12px; letter-spacing:.6px; text-transform:uppercase; color:#6b6b6b; margin:0 0 10px 0;">Login Information</div>
    #     <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
    #     <tbody><tr>
    #     <td style="padding:6px 0; width:160px; font-weight:600; color:#222;">Username:</td>
    #     <td style="padding:6px 0; color:#444;">USERNAME_PLACEHOLDER</td>
    #     </tr>
    #     <tr>
    #     <td style="padding:6px 0; width:160px; font-weight:600; color:#222;">Password:</td>
    #     <td style="padding:6px 0; color:#444;">PASSWORD_PLACEHOLDER</td>
    #     </tr>
    #     </tbody></table>
    #     </td>
    #     </tr>
    #     </tbody></table>
    #     <!-- Spacer -->
    #     <div style="height:18px; line-height:18px; font-size:0;"> </div>
    #     <!-- SECURITY -->
    #     <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="border:1px solid #ededed;">
    #     <tbody><tr>
    #     <td style="padding:16px;">
    #     <div style="font-size:12px; letter-spacing:.6px; text-transform:uppercase; color:#6b6b6b; margin:0 0 10px 0;">Security Information</div>
    #     <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
    #     <tbody><tr>
    #     <td style="padding:6px 0; width:160px; font-weight:600; color:#222;">Security Question:</td>
    #     <td style="padding:6px 0; color:#444;">SECURITY_QUESTION_PLACEHOLDER</td>
    #     </tr>
    #     <tr>
    #     <td style="padding:6px 0; width:160px; font-weight:600; color:#222;">Security Answer:</td>
    #     <td style="padding:6px 0; color:#444;">SECURITY_ANSWER_PLACEHOLDER</td>
    #     </tr>
    #     </tbody></table>
    #     </td>
    #     </tr>
    #     </tbody></table>
    #     </td>
    #     </tr>
    #     </tbody></table>
    #     </td>
    #     </tr>
    #     </tbody></table></div></td></tr><tr><td style="background-color:transparent;padding-top:14px;padding-bottom:12px;padding-right:24px;padding-left:24px;border:0;border-radius:0" valign="top" class="mceDividerBlockContainer" id="b25"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" role="presentation" class="mceDividerContainer" data-block-id="25"><tbody><tr><td style="min-width:100%;border-top-width:1px;border-top-style:solid;border-top-color:#e6e6e6;line-height:0;font-size:0" valign="top" class="mceDividerBlock"> </td></tr></tbody></table></td></tr><tr><td style="padding-top:12px;padding-bottom:12px;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" class="mceLayoutContainer" id="b26"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="26"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="24" width="100%" role="presentation"><tbody><tr><td valign="top" class="mceColumn" id="mceColumnId--6" data-block-id="-6" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="border:0;border-radius:0" valign="top" class="mceSocialFollowBlockContainer" id="b-5"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" class="mceSocialFollowBlock" data-block-id="-5"><tbody><tr><td valign="middle" align="center"><!--[if mso]><table align="left" border="0" cellspacing= "0" cellpadding="0"><tr><![endif]--><!--[if mso]><td align="center" valign="top"><![endif]--><table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;float:left" role="presentation"><tbody><tr><td style="padding-top:3px;padding-bottom:3px;padding-left:12px;padding-right:12px" valign="top" class="mceSocialFollowIcon" align="center" width="40"><a href="https://www.facebook.com/profile.php?id=61573573324144" target="_blank" rel="noreferrer"><img class="mceSocialFollowImage" width="40" height="40" alt="Facebook icon" src="https://cdn-images.mailchimp.com/icons/social-block-v3/block-icons-v3/facebook-filled-dark-40.png"/></a></td></tr></tbody></table><!--[if mso]></td><![endif]--><!--[if mso]><td align="center" valign="top"><![endif]--><table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;float:left" role="presentation"><tbody><tr><td style="padding-top:3px;padding-bottom:3px;padding-left:12px;padding-right:12px" valign="top" class="mceSocialFollowIcon" align="center" width="40"><a href="https://www.instagram.com/huse.ai?igsh=NmlqdWlxaHRydTdl" target="_blank" rel="noreferrer"><img class="mceSocialFollowImage" width="40" height="40" alt="Instagram icon" src="https://cdn-images.mailchimp.com/icons/social-block-v3/block-icons-v3/instagram-filled-dark-40.png"/></a></td></tr></tbody></table><!--[if mso]></td><![endif]--><!--[if mso]><td align="center" valign="top"><![endif]--><table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;float:left" role="presentation"><tbody><tr><td style="padding-top:3px;padding-bottom:3px;padding-left:12px;padding-right:12px" valign="top" class="mceSocialFollowIcon" align="center" width="40"><a href="https://x.com/huse_ai?t=9luOlwlTIWNWuxu9WV6SNQ&s=09" target="_blank" rel="noreferrer"><img class="mceSocialFollowImage" width="40" height="40" alt="X icon" src="https://cdn-images.mailchimp.com/icons/social-block-v3/block-icons-v3/twitter-filled-dark-40.png"/></a></td></tr></tbody></table><!--[if mso]></td><![endif]--><!--[if mso]></tr></table><![endif]--></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></tbody><tbody data-block-id="17" class="mceWrapper"><tr><td style="background-color:transparent" valign="top" align="center" class="mceSectionFooter"><!--[if (gte mso 9)|(IE)]><table align="center" border="0" cellspacing="0" cellpadding="0" width="660" style="width:660px;"><tr><td><![endif]--><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:660px" role="presentation"><tbody><tr><td style="background-color:#ffffff" valign="top" class="mceWrapperInner"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="16"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" id="mceColumnId--9" data-block-id="-9" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:8px;padding-bottom:8px;padding-right:8px;padding-left:8px;border:0;border-radius:0" valign="top" id="b15"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="15" id="section_fbe47c6f68c104faffe1abbb7d561a57" class="mceFooterSection"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="12" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" id="mceColumnId--3" data-block-id="-3" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" class="mceGutterContainer" id="gutterContainerId-13"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" align="center" id="b13"><table width="100%" style="border:0;background-color:transparent;border-radius:0;border-collapse:separate"><tbody><tr><td style="padding-left:16px;padding-right:16px;padding-top:12px;padding-bottom:12px" class="mceTextBlockContainer"><div data-block-id="13" class="mceText" id="d13" style="display:inline-block;width:100%"><p class="last-child"><span style="color:#6b6b6b;"><span style="font-size: 9px"><span style="font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif"><span style="background-color: rgb(255, 255, 255)">  © 2025 Hüse | </span></span></span></span><a href="mailto:info@huse.ai?subject=&body=" target="_blank" style="color: #6b6b6b; text-decoration: none;"><span style="font-size: 9px"><span style="font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif"><span style="background-color: rgb(255, 255, 255)">info@huse.ai</span></span></span></a></p></div></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td style="border:0;border-radius:0" valign="top" class="mceLayoutContainer" align="center" id="b-2"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="-2"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover;padding-top:0px;padding-bottom:0px" valign="top"><table border="0" cellpadding="0" cellspacing="24" width="100%" role="presentation"><tbody></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></tbody></table>
    #     </td>
    #     </tr>
    #     </tbody></table>
    #     </center>
    #     <script type="text/javascript"  src="/B-QdIp/Kr1/PBt/mK4ubA/iYkO4zSJGXmX2fObOf/dnwZFnQB/OVxn/TR1qAXoB"></script></body></html>
    #     """

    template = """
    <!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head>
    <!--[if gte mso 15]>
    <xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG/>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->
    <meta charset="UTF-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>*|MC:SUBJECT|*</title>
    <link rel="preconnect" href="https://fonts.googleapis.com"/>
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>
    <!--[if !mso]><!--><link rel="stylesheet" type="text/css" id="newGoogleFontsStatic" href="https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i,900,900i"/><!--<![endif]--><style>img{-ms-interpolation-mode:bicubic;}
    table, td{mso-table-lspace:0pt;mso-table-rspace:0pt;}
    .mceStandardButton, .mceStandardButton td, .mceStandardButton td a{mso-hide:all!important;}
    p, a, li, td, blockquote{mso-line-height-rule:exactly;}
    p, a, li, td, body, table, blockquote{-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%;}
    .mcnPreviewText{display:none!important;}
    .bodyCell{margin:0 auto;padding:0;width:100%;}
    .ExternalClass, .ExternalClass p, .ExternalClass td, .ExternalClass div, .ExternalClass span, .ExternalClass font{line-height:100%;}
    .ReadMsgBody, .ExternalClass{width:100%;}
    a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important;font-size:inherit!important;font-family:inherit!important;font-weight:inherit!important;line-height:inherit!important;}
    body{height:100%;margin:0;padding:0;width:100%;background:#ffffff;}
    p{margin:0;padding:0;}
    table{border-collapse:collapse;}
    td, p, a{word-break:break-word;}
    h1, h2, h3, h4, h5, h6{display:block;margin:0;padding:0;}
    img, a img{border:0;height:auto;outline:none;text-decoration:none;}
    a[href^="tel"], a[href^="sms"]{color:inherit;cursor:default;text-decoration:none;}
    .mceColumn .mceButtonLink,
                    .mceColumn-1 .mceButtonLink, 
                    .mceColumn-2 .mceButtonLink, 
                    .mceColumn-3 .mceButtonLink,
                    .mceColumn-4 .mceButtonLink{min-width:30px;}
    div[contenteditable="true"]{outline:0;}
    .mceImageBorder{display:inline-block;}
    .mceImageBorder img{border:0!important;}
    body, #bodyTable{background-color:rgb(244, 244, 244);}
    .mceText, .mcnTextContent, .mceLabel{font-family:"Helvetica Neue", Helvetica, Arial, Verdana, sans-serif;}
    .mceText, .mcnTextContent, .mceLabel{color:rgb(0, 0, 0);}
    .mceText h1, .mceText p, .mceText label, .mceText input{margin-bottom:0;}
    .mceSpacing-12 .mceInput + .mceErrorMessage{margin-top:-6px;}
    .mceSpacing-24 .mceInput + .mceErrorMessage{margin-top:-12px;}
    .mceInput{background-color:transparent;border:2px solid rgb(208, 208, 208);width:60%;color:rgb(77, 77, 77);display:block;}
    .mceInput[type="radio"], .mceInput[type="checkbox"]{float:left;margin-right:12px;display:inline;width:auto!important;}
    .mceLabel > .mceInput{margin-bottom:0;margin-top:2px;}
    .mceLabel{display:block;}
    .mceText p, .mcnTextContent p{color:rgb(0, 0, 0);font-family:"Helvetica Neue", Helvetica, Arial, Verdana, sans-serif;font-size:16px;font-weight:normal;line-height:1.5;mso-line-height-alt:150%;text-align:left;letter-spacing:0;direction:ltr;margin:0;}
    .mceText h1, .mcnTextContent h1{color:rgb(0, 0, 0);font-family:"Helvetica Neue", Helvetica, Arial, Verdana, sans-serif;font-size:31px;font-weight:bold;line-height:1.5;mso-line-height-alt:150%;text-align:left;letter-spacing:0;direction:ltr;}
    .mceText a, .mcnTextContent a{color:rgb(0, 0, 0);font-style:normal;font-weight:normal;text-decoration:underline;direction:ltr;}
    p.mcePastedContent, h1.mcePastedContent, h2.mcePastedContent, h3.mcePastedContent, h4.mcePastedContent{text-align:left;}
    #d13 p, #d13 h1, #d13 h2, #d13 h3, #d13 h4, #d13 ul{text-align:center;}
    @media only screen and (max-width: 480px) {
    body, table, td, p, a, li, blockquote{-webkit-text-size-adjust:none!important;}
    body{width:100%!important;min-width:100%!important;}
    body.mobile-native{-webkit-user-select:none;user-select:none;transition:transform 0.2s ease-in;transform-origin:top center;}
    colgroup{display:none;}
    .mceLogo img, .mceImage img, .mceSocialFollowIcon img{height:auto!important;}
    .mceWidthContainer{max-width:660px!important;}
    .mceColumn, .mceColumn-2{display:block!important;width:100%!important;}
    .mceColumn-forceSpan{display:table-cell!important;width:auto!important;}
    .mceColumn-forceSpan .mceButton a{min-width:0!important;}
    .mceReverseStack{display:table;width:100%;}
    .mceColumn-1{display:table-footer-group;width:100%!important;}
    .mceColumn-3{display:table-header-group;width:100%!important;}
    .mceColumn-4{display:table-caption;width:100%!important;}
    .mceKeepColumns .mceButtonLink{min-width:0;}
    .mceBlockContainer, .mceSpacing-24{padding-right:16px!important;padding-left:16px!important;}
    .mceBlockContainerE2E{padding-right:0;padding-left:0;}
    .mceImage, .mceLogo{width:100%!important;height:auto!important;}
    .mceText img{max-width:100%!important;}
    .mceFooterSection .mceText, .mceFooterSection .mceText p{font-size:16px!important;line-height:140%!important;}
    .mceText p{margin:0;font-size:16px!important;line-height:1.5!important;mso-line-height-alt:150%;}
    .mceText h1{font-size:31px!important;line-height:1.5!important;mso-line-height-alt:150%;}
    .bodyCell{padding-left:16px!important;padding-right:16px!important;}
    .mceDividerContainer{width:100%!important;}
    #b3, #gutterContainerId-13, #gutterContainerId-19, #gutterContainerId-33, #gutterContainerId-44, #gutterContainerId-45{padding:0!important;}
    #b3 table{margin-right:auto!important;float:none!important;}
    #b13 .mceTextBlockContainer{padding:12px 16px!important;}
    #b19 .mceTextBlockContainer{padding:0 24px 2px!important;}
    #b25 .mceDividerBlock{border-top-width:1px!important;}
    #b25{padding:14px 24px 12px!important;}
    #b33 .mceTextBlockContainer{padding:0 24px 18px!important;}
    #b44 .mceTextBlockContainer{padding:22px 42px!important;}
    #b45 .mceTextBlockContainer{padding:12px 24px!important;}
    }
    @media only screen and (max-width: 640px) {
    .mceClusterLayout td{padding:4px!important;}
    }</style></head>
    <body>
    <!--*|IF:MC_PREVIEW_TEXT|*-->
    <!--[if !gte mso 9]><!----><span class="mcnPreviewText" style="display:none; font-size:0px; line-height:0px; max-height:0px; max-width:0px; opacity:0; overflow:hidden; visibility:hidden; mso-hide:all;">*|MC_PREVIEW_TEXT|*</span><!--<![endif]-->
    <!--*|END:IF|*-->
    <div style="display: none; max-height: 0px; overflow: hidden;">͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌      ͏ ‌    ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­</div><!--MCE_TRACKING_PIXEL-->
    <center>
    <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="background-color: rgb(244, 244, 244);">
    <tbody><tr>
    <td class="bodyCell" align="center" valign="top">
    <table id="root" border="0" cellpadding="0" cellspacing="0" width="100%"><tbody data-block-id="5" class="mceWrapper"><tr><td style="background-color:transparent" valign="top" align="center" class="mceSectionHeader"><!--[if (gte mso 9)|(IE)]><table align="center" border="0" cellspacing="0" cellpadding="0" width="660" style="width:660px;"><tr><td><![endif]--><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:660px" role="presentation"><tbody><tr><td style="background-color:#ffffff" valign="top" class="mceWrapperInner"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="4"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" id="mceColumnId--9" data-block-id="-9" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="background-color:#ffffff;padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" class="mceImageBlockContainer" align="left" id="b3"><div><!--[if !mso]><!--></div><a href="http://www.huse.ai" style="display:block" target="_blank" data-block-id="3"><table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate;margin:0;vertical-align:top;max-width:100%;width:100%;height:auto" role="presentation" data-testid="image-3"><tbody><tr><td style="border:0;border-radius:0;margin:0" valign="top"><img alt="" src="https://mcusercontent.com/360a033fa9b35032b8dab5b54/images/c6916dd4-e56b-84e6-7baa-e5eb8ea7a16f.png" width="660" height="auto" style="display:block;max-width:100%;height:auto;border-radius:0" class="imageDropZone mceLogo"/></td></tr></tbody></table></a><div><!--<![endif]--></div><div>
    <!--[if mso]>
    <a href="http://www.huse.ai"><span class="mceImageBorder" style="border:0;border-width:2px;vertical-align:top;margin:0"><img role="presentation" class="imageDropZone mceLogo" src="https://mcusercontent.com/360a033fa9b35032b8dab5b54/images/c6916dd4-e56b-84e6-7baa-e5eb8ea7a16f.png" alt="" width="660" height="auto" style="display:block;max-width:660px;width:660px;height:auto"/></span></a>
    <![endif]-->
    </div></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></tbody><tbody data-block-id="11" class="mceWrapper"><tr><td style="background-color:transparent" valign="top" align="center" class="mceSectionBody"><!--[if (gte mso 9)|(IE)]><table align="center" border="0" cellspacing="0" cellpadding="0" width="660" style="width:660px;"><tr><td><![endif]--><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:660px" role="presentation"><tbody><tr><td style="background-color:#ffffff" valign="top" class="mceWrapperInner"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="10"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" id="mceColumnId--10" data-block-id="-10" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="background-color:transparent;border:0;border-radius:0" valign="top" id="b46"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="46"><tbody><tr><td valign="top" class="mceSpacerBlock" height="20"></td></tr></tbody></table></td></tr><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" class="mceGutterContainer" id="gutterContainerId-45"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" id="b45"><table width="100%" style="border:0;background-color:transparent;border-radius:0;border-collapse:separate"><tbody><tr><td style="padding-left:24px;padding-right:24px;padding-top:12px;padding-bottom:12px" class="mceTextBlockContainer"><div data-block-id="45" class="mceText" id="d45" style="width:100%"><h1 class="mcePastedContent last-child" style="line-height: 1; mso-line-height-alt: 100%;"><span style="font-size: 21px"><span style="font-family: Roboto, &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif">Welcome *FNAME|*,</span></span></h1></div></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" class="mceGutterContainer" id="gutterContainerId-19"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" id="b19"><table width="100%" style="border:0;background-color:transparent;border-radius:0;border-collapse:separate"><tbody><tr><td style="padding-left:24px;padding-right:24px;padding-top:0;padding-bottom:2px" class="mceTextBlockContainer"><div data-block-id="19" class="mceText" id="d19" style="width:100%"><p class="last-child"><span style="font-size: 13px"><span style="font-family: Roboto, &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif"><span style="font-weight:normal;">Your account has been successfully created. Please find your secure login credentials below. To get started, log in to the app and experience how HÜSE streamlines your daily work with AI.</span></span></span></p></div></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td style="border:0;border-radius:0" valign="top" id="b28"><div data-block-id="28" class="mceCode"><!-- Full width background -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#ffffff;">
    <tbody><tr>
    <td align="center" style="padding:40px 16px 10px 16px;">
    <!-- Constrained container -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width:620px; width:100%;">
    <tbody><tr>
    <td style="padding:0 24px;">
    <!-- Section header -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
    <tbody><tr>
    <td style="width:6px; background:#0b0b0b; border-radius:2px; line-height:0; font-size:0;"> </td>
    <td style="padding:0 12px;">
    <div style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:20px; font-weight:700; color:#0b0b0b; letter-spacing:.02em; line-height:1.3;">
    LOGIN INFORMATION
    </div>
    </td>
    </tr>
    </tbody></table>
    <div style="line-height:18px; height:18px;"> </div>
    <!-- Username card -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f6f7f9; border:1px solid #e5e7eb; border-radius:10px;">
    <tbody><tr>
    <td style="padding:18px 20px;">
    <div style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:12px; font-weight:700; color:#6b7280; letter-spacing:.12em; text-transform:uppercase; margin:0 0 10px 0;">
    Username
    </div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border:1px solid #e5e7eb; border-radius:8px;">
    <tbody><tr>
    <td style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:16px; color:#111827; padding:14px 16px;">
    *|USERNAME|*
    </td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table>
    <div style="line-height:18px; height:18px;"> </div>
    <!-- Password card -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f6f7f9; border:1px solid #e5e7eb; border-radius:10px;">
    <tbody><tr>
    <td style="padding:18px 20px;">
    <div style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:12px; font-weight:700; color:#6b7280; letter-spacing:.12em; text-transform:uppercase; margin:0 0 10px 0;">
    Password
    </div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border:1px solid #e5e7eb; border-radius:8px;">
    <tbody><tr>
    <td style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:16px; color:#111827; padding:14px 16px;">
    *|USERPASSWORD|*
    </td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table></div></td></tr><tr><td style="border:0;border-radius:0" valign="top" id="b30"><div data-block-id="30" class="mceCode"><title>Security Information</title>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#ffffff;">
    <tbody><tr>
    <td align="center" style="padding:40px 16px 10px 16px;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width:620px; width:100%;">
    <tbody><tr>
    <td style="padding:0 24px;">
    <!-- Section header -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
    <tbody><tr>
    <td style="width:6px; background:#0b0b0b; border-radius:2px; line-height:0; font-size:0;"> </td>
    <td style="padding:0 12px;">
    <div style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:20px; font-weight:700; color:#0b0b0b; letter-spacing:.02em; line-height:1.3;">
    SECURITY INFORMATION
    </div>
    </td>
    </tr>
    </tbody></table>
    <div style="line-height:18px; height:18px;"> </div>
    <!-- Security Question card -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f6f7f9; border:1px solid #e5e7eb; border-radius:10px;">
    <tbody><tr>
    <td style="padding:18px 20px;">
    <div style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:12px; font-weight:700; color:#6b7280; letter-spacing:.12em; text-transform:uppercase; margin:0 0 10px 0;">
    Security Question
    </div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border:1px solid #e5e7eb; border-radius:8px;">
    <tbody><tr>
    <td style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:16px; color:#111827; padding:14px 16px;">
    *|SECURITY_QUESTION|*
    </td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table>
    <div style="line-height:18px; height:18px;"> </div>
    <!-- Security Answer card -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f6f7f9; border:1px solid #e5e7eb; border-radius:10px;">
    <tbody><tr>
    <td style="padding:18px 20px;">
    <div style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:12px; font-weight:700; color:#6b7280; letter-spacing:.12em; text-transform:uppercase; margin:0 0 10px 0;">
    Security Answer
    </div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border:1px solid #e5e7eb; border-radius:8px;">
    <tbody><tr>
    <td style="font-family:Segoe UI, Roboto, Arial, sans-serif; font-size:16px; color:#111827; padding:14px 16px;">
    *|SECURITY_ANSWER|*
    </td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table>
    <div style="line-height:1px; height:1px;"> </div>
    </td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table></div></td></tr><tr><td valign="top" class="mceGutterContainer" id="gutterContainerId-39"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation"><tbody><tr><td style="padding-top:12px;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:12px" valign="top" class="mceLayoutContainer" id="b39"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="39" id="section_9f4416ede02c3d8cb1769e7a2252cd44" class="mceLayout"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td valign="top" class="mceColumn" id="mceColumnId--12" data-block-id="-12" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="border:0;border-radius:0" valign="top" align="center" id="b-8"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="-8"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td valign="top" class="mceColumn" id="mceColumnId--13" data-block-id="-13" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="border:0;border-radius:0" valign="top" id="b42"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="42"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="24" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" id="mceColumnId-41" data-block-id="41" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" class="mceGutterContainer" id="gutterContainerId-44"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" id="b44"><table width="100%" style="border:0;background-color:#000000;border-radius:0;border-collapse:separate"><tbody><tr><td style="padding-left:42px;padding-right:42px;padding-top:22px;padding-bottom:22px" class="mceTextBlockContainer"><div data-block-id="44" class="mceText" id="d44" style="width:100%"><p class="mcePastedContent"><strong><span style="color:rgb(255, 255, 255);"><span style="font-family: Roboto, &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif">Important Security Notice</span></span></strong></p><p class="mcePastedContent last-child"><span style="color:rgb(255, 255, 255);"><span style="font-size: 12px"><span style="font-family: Roboto, &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif">Please keep your login credentials confidential and secure. If you suspect unauthorized access, contact IT Support immediately.</span></span></span></p></div></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td style="background-color:transparent;border:0;border-radius:0" valign="top" id="b34"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="34"><tbody><tr><td valign="top" class="mceSpacerBlock" height="20"></td></tr></tbody></table></td></tr><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" class="mceGutterContainer" id="gutterContainerId-33"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" id="b33"><table width="100%" style="border:0;background-color:transparent;border-radius:0;border-collapse:separate"><tbody><tr><td style="padding-left:24px;padding-right:24px;padding-top:0;padding-bottom:18px" class="mceTextBlockContainer"><div data-block-id="33" class="mceText" id="d33" style="width:100%"><p class="last-child"><span style="font-size: 13px"><span style="font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif">Best Regards,<br/></span></span><strong><span style="font-size: 13px"><span style="font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif">Team </span><span style="font-family: Roboto, &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif">HÜSE</span></span></strong></p></div></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td style="background-color:transparent;padding-top:14px;padding-bottom:12px;padding-right:24px;padding-left:24px;border:0;border-radius:0" valign="top" class="mceDividerBlockContainer" id="b25"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" role="presentation" class="mceDividerContainer" data-block-id="25"><tbody><tr><td style="min-width:100%;border-top-width:1px;border-top-style:solid;border-top-color:#e6e6e6;line-height:0;font-size:0" valign="top" class="mceDividerBlock"> </td></tr></tbody></table></td></tr><tr><td style="padding-top:12px;padding-bottom:12px;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" class="mceLayoutContainer" id="b26"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="26"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="24" width="100%" role="presentation"><tbody><tr><td valign="top" class="mceColumn" id="mceColumnId--6" data-block-id="-6" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="border:0;border-radius:0" valign="top" class="mceSocialFollowBlockContainer" id="b-5"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" class="mceSocialFollowBlock" data-block-id="-5"><tbody><tr><td valign="middle" align="center"><!--[if mso]><table align="left" border="0" cellspacing= "0" cellpadding="0"><tr><![endif]--><!--[if mso]><td align="center" valign="top"><![endif]--><table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;float:left" role="presentation"><tbody><tr><td style="padding-top:3px;padding-bottom:3px;padding-left:12px;padding-right:12px" valign="top" class="mceSocialFollowIcon" align="center" width="40"><a href="https://www.facebook.com/profile.php?id=61573573324144" target="_blank" rel="noreferrer"><img class="mceSocialFollowImage" width="40" height="40" alt="Facebook icon" src="https://cdn-images.mailchimp.com/icons/social-block-v3/block-icons-v3/facebook-filled-dark-40.png"/></a></td></tr></tbody></table><!--[if mso]></td><![endif]--><!--[if mso]><td align="center" valign="top"><![endif]--><table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;float:left" role="presentation"><tbody><tr><td style="padding-top:3px;padding-bottom:3px;padding-left:12px;padding-right:12px" valign="top" class="mceSocialFollowIcon" align="center" width="40"><a href="https://www.instagram.com/huse.ai?igsh=NmlqdWlxaHRydTdl" target="_blank" rel="noreferrer"><img class="mceSocialFollowImage" width="40" height="40" alt="Instagram icon" src="https://cdn-images.mailchimp.com/icons/social-block-v3/block-icons-v3/instagram-filled-dark-40.png"/></a></td></tr></tbody></table><!--[if mso]></td><![endif]--><!--[if mso]><td align="center" valign="top"><![endif]--><table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;float:left" role="presentation"><tbody><tr><td style="padding-top:3px;padding-bottom:3px;padding-left:12px;padding-right:12px" valign="top" class="mceSocialFollowIcon" align="center" width="40"><a href="https://x.com/huse_ai?t=9luOlwlTIWNWuxu9WV6SNQ&s=09" target="_blank" rel="noreferrer"><img class="mceSocialFollowImage" width="40" height="40" alt="X icon" src="https://cdn-images.mailchimp.com/icons/social-block-v3/block-icons-v3/twitter-filled-dark-40.png"/></a></td></tr></tbody></table><!--[if mso]></td><![endif]--><!--[if mso]></tr></table><![endif]--></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></tbody><tbody data-block-id="17" class="mceWrapper"><tr><td style="background-color:transparent" valign="top" align="center" class="mceSectionFooter"><!--[if (gte mso 9)|(IE)]><table align="center" border="0" cellspacing="0" cellpadding="0" width="660" style="width:660px;"><tr><td><![endif]--><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:660px" role="presentation"><tbody><tr><td style="background-color:#ffffff" valign="top" class="mceWrapperInner"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="16"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" id="mceColumnId--11" data-block-id="-11" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:8px;padding-bottom:8px;padding-right:8px;padding-left:8px;border:0;border-radius:0" valign="top" id="b15"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="15" id="section_3813fd32edfa6bc167f67cb0f11ba428" class="mceFooterSection"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top"><table border="0" cellpadding="0" cellspacing="12" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" id="mceColumnId--3" data-block-id="-3" colspan="12" width="100%"><table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" class="mceGutterContainer" id="gutterContainerId-13"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation"><tbody><tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" align="center" id="b13"><table width="100%" style="border:0;background-color:transparent;border-radius:0;border-collapse:separate"><tbody><tr><td style="padding-left:16px;padding-right:16px;padding-top:12px;padding-bottom:12px" class="mceTextBlockContainer"><div data-block-id="13" class="mceText" id="d13" style="display:inline-block;width:100%"><p style="text-align: center;" class="last-child"><span style="color:#6b6b6b;"><span style="font-size: 9px"><span style="font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif"><span style="background-color: rgb(255, 255, 255)">  © 2025 </span></span></span></span><span style="color:rgb(107, 107, 107);"><span style="font-size: 9px"><span style="font-family: Roboto, &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif"><span style="background-color: rgb(255, 255, 255)">HÜSE</span></span></span></span><span style="color:#6b6b6b;"><span style="font-size: 9px"><span style="font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif"><span style="background-color: rgb(255, 255, 255)"> | </span></span></span></span><a href="mailto:info@huse.ai?subject=&body=" target="_blank" style="color: #6b6b6b;"><span style="font-size: 9px"><span style="font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif"><span style="background-color: rgb(255, 255, 255)">info@huse.ai</span></span></span></a></p></div></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td style="border:0;border-radius:0" valign="top" class="mceLayoutContainer" align="center" id="b-2"><table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="-2"><tbody><tr class="mceRow"><td style="background-position:center;background-repeat:no-repeat;background-size:cover;padding-top:0px;padding-bottom:0px" valign="top"><table border="0" cellpadding="0" cellspacing="24" width="100%" role="presentation"><tbody></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]--></td></tr></tbody></table>
    </td>
    </tr>
    </tbody></table>
    </center>
    <script type="text/javascript"  src="/bByYwmfSu6clOtn3I-XaPX61FXo/ri3StJpw6mQSGkiY/AT9EIQ0C/eD/4mS2sjWlc"></script></body></html>
    """
    return template.replace('*|MC:SUBJECT|*', subject).replace('*FNAME|*', employee_name).replace('*|USERNAME|*', username).replace('*|USERPASSWORD|*', password).replace('*|SECURITY_QUESTION|*', security_question).replace('*|SECURITY_ANSWER|*', security_answer).replace('*|MC_PREVIEW_TEXT|*', preview_text)
