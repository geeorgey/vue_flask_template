(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2916a420"],{"0d49":function(t,e,o){},5326:function(t,e,o){"use strict";o.r(e);var a=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("v-container",{staticClass:"page-login",attrs:{"fill-height":""}},[o("v-row",[o("v-col",{attrs:{cols:12}},[o("v-card",{staticClass:"pa-3 page-login__card",attrs:{tile:""}},[o("v-card-title",[o("img",{attrs:{src:"/static/m.png",alt:"Vue Material Admin",height:"48",contain:""}}),o("div",{staticClass:"primary--text display-1"},[t._v("Vue.js Flask template")])]),o("v-card-text",[o("v-form",{ref:"form",staticClass:"my-10",attrs:{"lazy-validation":""},model:{value:t.formValid,callback:function(e){t.formValid=e},expression:"formValid"}},[o("v-text-field",{attrs:{"append-icon":"mdi-email",autocomplete:"off",name:"login",label:t.$t("username"),placeholder:t.$t("username"),type:"text",required:"",outlined:"",rules:t.formRule.username},model:{value:t.formModel.username,callback:function(e){t.$set(t.formModel,"username",e)},expression:"formModel.username"}}),o("v-text-field",{attrs:{"append-icon":"mdi-lock",autocomplete:"off",name:"password",label:t.$t("password"),placeholder:t.$t("password"),type:"password",rules:t.formRule.password,required:"",outlined:""},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.handleLogin.apply(null,arguments)}},model:{value:t.formModel.password,callback:function(e){t.$set(t.formModel,"password",e)},expression:"formModel.password"}})],1)],1),o("v-card-actions",[t._l(t.socialIcons,(function(e){return o("v-tooltip",{key:e.text,attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var r=a.on,n=a.attrs;return[o("v-btn",t._g(t._b({attrs:{color:"primary",icon:""},on:{click:t.handleSocialLogin}},"v-btn",n,!1),r),[o("v-icon",{domProps:{textContent:t._s(e.icon)}})],1)]}}],null,!0)},[o("span",[t._v(t._s(e.text))])])})),o("v-spacer"),o("v-btn",{attrs:{large:"",text:""},on:{click:t.handleRegister}},[t._v(" "+t._s(t.$t("register"))+" ")]),o("v-btn",{attrs:{large:"",tile:"",color:"primary",loading:t.loading},on:{click:t.handleLogin}},[t._v(" "+t._s(t.$t("login"))+" ")])],2)],1)],1)],1)],1)},r=[],n="page-login",i={name:n,data:function(){var t=this;return{loading:!1,formValid:!1,formModel:{username:"admin",password:"admin"},formRule:{username:[function(e){return!!e||t.$t("rule.required",["username"])}],password:[function(e){return!!e||t.$t("rule.required",["password"])}]},socialIcons:[{text:"Google",icon:"mdi-google"},{text:"Facebook",icon:"mdi-facebook"},{text:"Twitter",icon:"mdi-twitter"}]}},computed:{},methods:{handleLogin:function(){var t=this;this.$refs.form.validate()&&(this.loading=!0,this.$store.dispatch("login",this.formModel).then((function(){t.$route.query.redirect;t.loading=!1,t.$router.push("/dashboard")}))["catch"]((function(){window._VMA.$emit("SHOW_SNACKBAR",{show:!0,text:"Auth Failed",color:"error"}),t.loading=!1})))},handleRegister:function(){var t=this;console.log(this),this.$refs.form.validate()&&(this.loading=!0,this.$store.dispatch("register",this.formModel).then((function(){var e=t.$route.query.redirect,o=e?{path:e}:{path:"/"};t.$router.push(o),t.loading=!1}))["catch"]((function(){window._VMA.$emit("SHOW_SNACKBAR",{show:!0,text:"Auth Failed",color:"error"}),t.loading=!1})))},handleSocialLogin:function(){}}},l=i,s=(o("99df"),o("2877")),d=o("6544"),c=o.n(d),u=o("8336"),f=o("b0af"),m=o("99d9"),p=o("62ad"),h=o("a523"),g=o("4bd4"),v=o("132d"),w=o("0fd9"),b=o("2fa4"),x=o("8654"),V=o("3a2f"),$=Object(s["a"])(l,a,r,!1,null,"4b1ea1c2",null);e["default"]=$.exports;c()($,{VBtn:u["a"],VCard:f["a"],VCardActions:m["a"],VCardText:m["b"],VCardTitle:m["c"],VCol:p["a"],VContainer:h["a"],VForm:g["a"],VIcon:v["a"],VRow:w["a"],VSpacer:b["a"],VTextField:x["a"],VTooltip:V["a"]})},"99df":function(t,e,o){"use strict";o("0d49")}}]);