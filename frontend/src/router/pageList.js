// page list config
import IndexPage from "@/pages/IndexPage"

import LoginPage from "@/pages/LoginPage"
import RegisterPage from "@/pages/RegisterPage"

import PostDetail from "@/pages/PostDetail"
import SearchList from "@/pages/SearchList"

const pageList = {
    "/": {
        title: "首页/搜索",
        name: "index",
        component: IndexPage
    },
    "login": {
        title: "登录",
        name: "login",
        component: LoginPage
    },
    "register": {
        title: "注册",
        name: "register",
        component: RegisterPage
    },
    "search": {
        title: "资讯列表",
        name: "search",
        component: SearchList
    },
    "post/detail/:id(\\d+)": {
        title: "资讯详情",
        name: "post_detail",
        component: PostDetail
    },
};

export default pageList;