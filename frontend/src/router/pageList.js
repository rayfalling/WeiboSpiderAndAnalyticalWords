// page list config
import LoginPage from "@/pages/LoginPage"
import RegisterPage from "@/pages/RegisterPage"

const pageList = {
    "/": {
        title: "登录",
        name: "login",
        component: LoginPage
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
    // information: {
    //     title: "详情",
    //     name: "information",
    //     component: Information
    // },
    // about: {
    //     title: "关于",
    //     name: "about",
    //     component: About
    // },
    // more: {
    //     title: "更多",
    //     name: "more",
    //     subpages: {
    //         setting: {
    //             title: "设置",
    //             name: "setting",
    //             component: Setting
    //         },
    //         other: {
    //             title: "其他",
    //             name: "other",
    //             component: Other
    //         },
    //     }
    // }
};

export default pageList;