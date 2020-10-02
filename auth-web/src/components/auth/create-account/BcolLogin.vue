<template>
  <v-form ref="form" lazy-validation >
    <fieldset>
      <legend class="mb-3">
        BC Online Prime Contact Details
        <v-tooltip bottom color="grey darken-4">
          <template v-slot:activator="{ on }">
            <v-icon color="grey darken-4" v-on="on" tabindex="0">mdi-help-circle-outline</v-icon>
          </template>
          <div class="bcol-tooltip__msg py-2">BC Online Prime Contacts are users who have authority to manage account settings for a BC Online Account.</div>
        </v-tooltip>
      </legend>
      <v-slide-y-transition>
        <div class="pb-2" v-show="errorMessage">
          <v-alert type="error" icon="mdi-alert-circle-outline">
            {{errorMessage}}
          </v-alert>
        </div>
      </v-slide-y-transition>
      <v-row>
        <v-col cols="4" class="py-0 pr-0">
          <v-text-field
                  filled
                  label="User ID"
                  v-model.trim="username"
                  :rules="usernameRules"
                  req
                  dense
          >
          </v-text-field>
        </v-col>
        <v-col cols="4" class="py-0 pr-0">
          <v-text-field
                  filled
                  label="Password"
                  v-model.trim="password"
                  req
                  dense
                  :rules="passwordRules"
          >
          </v-text-field>
        </v-col>
        <v-col cols="4" class="py-0">
          <v-btn
            x-large
            depressed
            color="primary"
            class="link-account-btn"
            @click="linkAccounts()"
            data-test="dialog-save-button"
            :loading="isLoading"
            :disabled='!isFormValid() || isLoading'
          >
            Link Account
          </v-btn>
        </v-col>
      </v-row>
    </fieldset>
  </v-form>
</template>

<script lang="ts">
import { BcolAccountDetails, BcolProfile } from '@/models/bcol'
import { Component, Emit, Prop, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
@Component({
  name: 'BcolLogin',
  computed: {
    ...mapState('org', ['currentOrganization'])
  },
  methods: {
    ...mapActions('org', ['createOrg', 'syncMembership', 'syncOrganization', 'validateBcolAccount'])
  }
})
export default class BcolLogin extends Vue {
  private username: string = ''
  private password: string = ''
  private errorMessage: string = ''
  private isLoading: boolean = false
  private readonly validateBcolAccount!: (bcolProfile: BcolProfile) => Promise<BcolAccountDetails>

  private isFormValid (): boolean {
    return !!this.username && !!this.password
  }
  private usernameRules = [
    v => !!v.trim() || 'Username is required'
  ]

  private passwordRules = [
    value => !!value || 'Password is required'
  ]

  $refs: {
    form: HTMLFormElement
  }

  private async linkAccounts () {
    this.isLoading = true
    this.errorMessage = ''
    // Validate form, and then create an team with this user a member
    if (this.isFormValid()) {
      const bcolProfile: BcolProfile = {
        userId: this.username,
        password: this.password
      }
      try {
        const bcolAccountDetails = await this.validateBcolAccount(bcolProfile)
        this.isLoading = false
        if (bcolAccountDetails) { // TODO whats the success status
          this.$emit('account-link-successful', { bcolProfile, bcolAccountDetails })
          this.resetForm()
        }
      } catch (err) {
        this.isLoading = false
        switch (err.response.status) {
          case 409:
            this.errorMessage = err.response.data.message
            break
          case 400:
            this.errorMessage = err.response.data.message
            break
          default:
            this.errorMessage = 'An error occurred while attempting to create your account.'
        }
      }
    }
  }
  resetForm () {
    this.username = this.password = this.errorMessage = ''
    this.$refs.form.resetValidation()
  }
}
</script>

<style lang="scss" scoped>
  .bcol-tooltip__msg {
    max-width: 20rem;
    line-height: 1.5;
    font-size: 0.9375rem;
  }

  .v-icon {
    margin-top: -2px;
    font-size: 1.25rem !important;
  }

  .v-btn.link-account-btn {
    font-size: 0.875rem !important;
    font-weight: 700;
  }

  .v-tooltip__content:before {
    content: ' ';
    position: absolute;
    top: -20px;
    left: 50%;
    margin-left: -10px;
    width: 20px;
    height: 20px;
    border-width: 10px 10px 10px 10px;
    border-style: solid;
    border-color: transparent transparent var(--v-grey-darken4) transparent;
  }
</style>