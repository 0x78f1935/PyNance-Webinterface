<template>
    <v-row>
        <v-col class="mt-2" cols="12">
            <strong>Backup</strong>
        </v-col>
        <v-col cols="6" md="2">
            
            

            <v-card
                :loading="loading"
                class="mx-auto my-12 img"
                max-width="374"
            >
                <template slot="progress">
                    <v-progress-linear
                        color="accent"
                        height="10"
                        indeterminate
                    ></v-progress-linear>
                </template>

                <v-icon size="250">mdi-download</v-icon>
                
                <v-card-text>
                    <v-checkbox
                        v-model="backup_passwords"
                        label="Backup passwords"
                    ></v-checkbox>
                </v-card-text>
                <v-card-actions>
                    <v-btn @click="downloadBackup" :disabled="loading" width="100%">Download backup</v-btn>
                </v-card-actions>
            </v-card>
        </v-col>

        <v-col cols="6" md="2">
            <v-card
                :loading="loading"
                class="mx-auto my-12 img"
                max-width="374"
            >
                <template slot="progress">
                    <v-progress-linear
                        color="accent"
                        height="10"
                        indeterminate
                    ></v-progress-linear>
                </template>

                <v-icon size="250">mdi-backup-restore</v-icon>

                <v-card-text>
                    <v-file-input
                        accept=".pynance"
                        label="Restore backup"
                        :disabled="loading"
                        v-model="backupfile"
                        truncate-length="10"
                    ></v-file-input>
                </v-card-text>

                <v-card-actions>
                    <v-btn @click="restoreBackup" :disabled="loading" width="100%">Restore backup</v-btn>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
    export default {
        name: 'backup',
        data() {
            return {
                backup_passwords: false,
                backupfile: null
            }
        },
        methods: {
            downloadBackup() {
                this.$store.dispatch('backup', this.$data.backup_passwords);
            },
            restoreBackup() {
                this.$store.dispatch('restore', {
                    backup: this.$data.backupfile, 
                });
            },
        },
        computed: {
            loading() {
                return this.$store.getters.backupping;
            }
        },
    }
</script>

<style lang="scss" scoped>
.img{
    text-align: center !important;
}
</style>