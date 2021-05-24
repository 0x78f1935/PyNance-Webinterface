import { Module } from "vuex";
import axios from 'axios';
import router from "@/router";

const BackupModule: Module<any, any> = { 
    state: {
        backupping: false,
    },

    getters: {
        backupping: state => state.backupping,
    },

    mutations: {
        SET_BACKUPPING(state, value) { state.backupping = value; },
    },
    actions: {
        backup(state, value) {
            if(state.getters.authenticated){
                state.commit('SET_BACKUPPING', true);
                axios.get(`/api/v1/backup?pwd=${value}`, {responseType: 'blob', headers: {'token': state.getters.token}}).then(response => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    const fileName = `backup_${+ new Date()}.pynance`// whatever your file name .
                    link.setAttribute('download', fileName);
                    document.body.appendChild(link);
                    link.click();
                    link.remove();// you need to remove that elelment which is created before.
                    state.commit('SET_BACKUPPING', false);
                })
            }
        },
        restore(state, data) {
            state.commit('SET_BACKUPPING', true);
            const formdata = new FormData();
            formdata.append('backup', data.backup);
            axios.post(`/api/v1/backup/`, formdata, {
                headers: {
                'Content-Type': 'application/zip',
                'token': state.getters.token
                }
            }).then((response) => {
                alert(response.data.msg);
                router.go(0);
            });
        }
    }
}

export default BackupModule;
