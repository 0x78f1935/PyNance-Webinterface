import { Module } from "vuex";
import axios from 'axios';

const BackupModule: Module<any, any> = { 
    actions: {
        backup(state, value) {
            if(state.getters.authenticated){
                axios.get(`/api/v1/backup?pwd=${value}`, {responseType: 'blob', headers: {'token': state.getters.token}}).then(response => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    const fileName = `backup_${+ new Date()}.pynance`// whatever your file name .
                    link.setAttribute('download', fileName);
                    document.body.appendChild(link);
                    link.click();
                    link.remove();// you need to remove that elelment which is created before.
                });
            }
        },
        restore(state, data) {
            const formdata = new FormData();
            formdata.append('backup', data.backup);
            axios.post(`/api/v1/backup/`, formdata, {
                headers: {
                'Content-Type': 'application/zip',
                'token': state.getters.token
                }
            }).then((response) => {
                alert(response.data.msg);
            });
        }
    }
}

export default BackupModule;
