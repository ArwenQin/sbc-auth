<template>
  <v-form
    ref="form"
    lazy-validation
    data-test="form-profile"
  >
    <p
      v-if="isStepperView"
      class="mb-9 profile-subtitle"
    >
      Enter your contact information. Once your account is created, you may add additional users and assign roles.
    </p>
    <p
      v-if="isAffidavitUpload"
      class="mb-7 profile-subtitle"
    >
      This will be reviewed by Registries staff and the account will be approved
      when authenticated.
    </p>
    <v-expand-transition>
      <div
        v-show="formError"
        class="form_alert-container"
      >
        <v-alert
          type="error"
          class="mb-3"
          :value="true"
        >
          {{ formError }}
        </v-alert>
      </div>
    </v-expand-transition>
    <!-- First / Last Name -->
    <v-row v-if="isInEditNameMode">
      <v-col
        cols="6"
        class="py-0"
      >
        <v-text-field
          v-model="firstName"
          filled
          label="First Name"
          req
          persistent-hint
          hint="Your first name as it appears on your affidavit"
          :rules="firstNameRules"
          data-test="firstName"
        />
      </v-col>
      <v-col
        cols="6"
        class="py-0"
      >
        <v-text-field
          v-model="lastName"
          filled
          label="Last Name"
          req
          persistent-hint
          hint="Your last name as it appears on your affidavit"
          :rules="lastNameRules"
          data-test="lastName"
        />
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col
        cols="12"
        class="py-0 mb-4"
      >
        <h4
          :class="{'legal-name': !isStepperView}"
          class="mb-1"
        >
          {{ firstName }} {{ lastName }}
        </h4>
        <div
          v-if="!isBCEIDUser"
          class="mb-2 profile-subtitle"
        >
          This is your legal name as it appears on your BC Services Card.
        </div>
      </v-col>
    </v-row>
    <!-- Email Address -->
    <v-row>
      <v-col
        cols="12"
        class="pt-0 pb-0"
      >
        <v-text-field
          v-model="emailAddress"
          filled
          label="Email Address"
          req
          persistent-hint
          :rules="emailRules"
          data-test="email"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        class="pt-0 pb-0"
      >
        <v-text-field
          v-model="confirmedEmailAddress"
          filled
          label="Confirm Email Address"
          req
          persistent-hint
          :error-messages="emailMustMatch()"
          data-test="confirm-email"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        md="6"
        class="pt-0 pb-0"
      >
        <v-text-field
          v-model="phoneNumber"
          v-mask="['(###) ###-####']"
          filled
          label="Phone Number"
          persistent-hint
          type="tel"
          hint="Example: (555) 555-5555"
          :rules="phoneRules"
          data-test="phone"
        />
      </v-col>
      <v-col
        cols="12"
        md="3"
        class="pt-0 pb-0"
      >
        <v-text-field
          v-model="extension"
          v-mask="'#####'"
          filled
          label="Extension"
          persistent-hint
          :rules="extensionRules"
          data-test="phone-extension"
        />
      </v-col>
    </v-row>

    <v-divider class="mt-7 mb-10" />

    <v-row>
      <v-col
        cols="12"
        class="form__btns py-0 d-inline-flex"
      >
        <!-- The deactivate profile button should be hidden for account stepper view and for admin affidavit BCeId flow -->
        <v-btn
          v-show="editing && !isStepperView && !isAffidavitUpload"
          large
          depressed
          color="default"
          class="deactivate-btn"
          data-test="btn-profile-deactivate"
          @click="$refs.deactivateUserConfirmationDialog.open()"
        >
          Deactivate my profile
        </v-btn>
        <!-- The reset button should be hidden in Production environment and who doesn't have tester role and for admin affidavit BCeId flow  -->
        <v-btn
          v-show="editing && !isStepperView && isTester && !isAffidavitUpload"
          large
          depressed
          color="default"
          class="reset-btn"
          data-test="btn-profile-reset"
          @click="$refs.resetDialog.open()"
        >
          Reset
        </v-btn>
        <v-btn
          v-if="isStepperView || isAffidavitUpload"
          large
          outlined
          color="primary"
          data-test="btn-back"
          @click="goBack"
        >
          <v-icon
            left
            class="mr-2"
          >
            mdi-arrow-left
          </v-icon>
          <span>Back</span>
        </v-btn>
        <v-spacer />
        <v-btn
          v-if="!isStepperView || isAffidavitUpload"
          large
          color="primary"
          class="save-continue-button mr-2"
          :disabled="!isFormValid()"
          data-test="save-button"
          @click="save"
        >
          {{ isAffidavitUpload ? 'Submit' : 'Save' }}
        </v-btn>
        <v-btn
          v-if="isStepperView"
          large
          color="primary"
          class="save-continue-button mr-3"
          :disabled="!isFormValid()"
          data-test="next-button"
          @click="next"
        >
          <span>
            Next
            <v-icon class="ml-2">mdi-arrow-right</v-icon>
          </span>
        </v-btn>
        <ConfirmCancelButton
          v-if="!isAffidavitUpload"
          :showConfirmPopup="isStepperView"
          :isEmit="true"
          :newStyleStepper="true"
          @click-confirm="cancel"
        />
      </v-col>
    </v-row>

    <!-- Modal for deactivation confirmation -->
    <ModalDialog
      ref="deactivateUserConfirmationDialog"
      :title="$t('deactivateConfirmTitle')"
      dialog-class="notify-dialog"
      max-width="640"
    >
      <template #icon>
        <v-icon
          large
          color="error"
        >
          mdi-alert-circle-outline
        </v-icon>
      </template>
      <template #text>
        <p class="pb-1">
          {{ $t('deactivateConfirmText') }} <strong>{{ $t('deactivateConfirmTextEmphasis') }}</strong>
        </p>
      </template>
      <template #actions>
        <v-btn
          large
          color="error"
          :loading="isDeactivating"
          data-test="deactivate-confirm-button"
          @click="deactivate()"
        >
          Deactivate
        </v-btn>
        <v-btn
          large
          color="default"
          :disabled="isDeactivating"
          data-test="deactivate-cancel-button"
          @click="cancelConfirmDeactivate()"
        >
          Cancel
        </v-btn>
      </template>
    </ModalDialog>

    <!-- Modal for deactivation failure -->
    <ModalDialog
      ref="deactivateUserFailureDialog"
      :title="$t('deactivateFailureTitle')"
      :text="$t('deactivateFailureText')"
      dialog-class="notify-dialog"
      max-width="640"
    >
      <template #icon>
        <v-icon
          large
          color="error"
        >
          mdi-alert-circle-outline
        </v-icon>
      </template>
    </ModalDialog>

    <!-- Modal for Reset  -->
    <ModalDialog
      ref="resetDialog"
      :title="$t('resetConfirmTitle')"
      :text="$t('resetConfirmText')"
      dialog-class="notify-dialog"
      max-width="640"
    >
      <template #icon>
        <v-icon
          large
          color="error"
        >
          mdi-alert-circle-outline
        </v-icon>
      </template>
      <template #text>
        <p class="pb-1">
          {{ $t('resetConfirmText') }} <strong>{{ $t('resetConfirmTextEmphasis') }}</strong>
        </p>
      </template>
      <template #actions>
        <v-btn
          large
          color="error"
          :loading="isReseting"
          data-test="reset-confirm-button"
          @click="reset()"
        >
          Reset
        </v-btn>
        <v-btn
          large
          color="default"
          :disabled="isReseting"
          data-test="reset-cancel-button"
          @click="cancelConfirmReset()"
        >
          Cancel
        </v-btn>
      </template>
    </ModalDialog>

    <!-- Modal for reset failure -->
    <ModalDialog
      ref="resetFailureDialog"
      :title="$t('resetFailureTitle')"
      :text="$t('resetFailureText')"
      dialog-class="notify-dialog"
      max-width="640"
    >
      <template #icon>
        <v-icon
          large
          color="error"
        >
          mdi-alert-circle-outline
        </v-icon>
      </template>
    </ModalDialog>
  </v-form>
</template>

<script lang="ts">
import { AccessType, Account, LoginSource, Pages, Role } from '@/util/constants'
import { Component, Emit, Mixins, Prop } from 'vue-property-decorator'
import { User, UserProfileData } from '@/models/user'
import { mapActions, mapState } from 'pinia'
import CommonUtils from '@/util/common-util'
import ConfirmCancelButton from '@/components/auth/common/ConfirmCancelButton.vue'
import { Contact } from '@/models/contact'
import ModalDialog from '@/components/auth/common/ModalDialog.vue'
import NextPageMixin from '@/components/auth/mixins/NextPageMixin.vue'
import Steppable from '@/components/auth/common/stepper/Steppable.vue'
import UserService from '@/services/user.services'
import { appendAccountId } from 'sbc-common-components/src/util/common-util'
import configHelper from '@/util/config-helper'
import { mask } from 'vue-the-mask'
import { useOrgStore } from '@/stores/org'
import { useUserStore } from '@/stores/user'

@Component({
  components: {
    ModalDialog,
    ConfirmCancelButton
  },
  directives: {
    mask
  },
  computed: {
    ...mapState(useOrgStore, ['currentOrganization']),
    ...mapState(useUserStore, [
      'userProfileData'
    ])
  },
  methods: {
    ...mapActions(useUserStore,
      [
        'createUserContact',
        'updateUserContact',
        'getUserProfile',
        'createAffidavit',
        'updateUserFirstAndLastName',
        'setUserProfileData',
        'setUserProfile'
      ]),
    ...mapActions(useOrgStore, ['syncMembership', 'syncOrganization'])
  }
})
export default class UserProfileForm extends Mixins(NextPageMixin, Steppable) {
    @Prop({ default: false }) isAffidavitUpload: boolean
    @Prop() token: string
    private readonly createUserContact!: (contact?: Contact) => Contact
    private readonly updateUserContact!: (contact?: Contact) => Contact
    private readonly getUserProfile!: (identifer: string) => User
    private readonly updateUserFirstAndLastName!: (user?: User) => Contact
    private readonly setUserProfileData!: (userProfile: UserProfileData | undefined) => void
    private firstName = ''
    private lastName = ''
    private emailAddress = ''
    private confirmedEmailAddress = ''
    private phoneNumber = ''
    private extension = ''
    private formError = ''
    private editing = false
    private deactivateProfileDialog = false
    private isDeactivating = false
    readonly userProfileData!: UserProfileData
    private readonly ACCOUNT_TYPE = Account
    private isTester: boolean = false
    private isReseting = false

    // this prop is used for conditionally using this form in both account stepper and edit profile pages
    @Prop({ default: false }) isStepperView: boolean
    @Prop({ default: AccessType.REGULAR }) stepperSource: string
    // need to cleat user profile in stepper BCEID re-upload time. if need to reset profile pass this
    @Prop({ default: false }) clearForm: boolean

    $refs: {
      deactivateUserConfirmationDialog: InstanceType<typeof ModalDialog>,
      deactivateUserFailureDialog: InstanceType<typeof ModalDialog>,
      resetDialog: InstanceType<typeof ModalDialog>,
      resetFailureDialog: InstanceType<typeof ModalDialog>,
      form: HTMLFormElement
    }

    private emailRules = [
      v => !!v || 'Email address is required',
      v => {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return pattern.test(v) || 'Valid email is required'
      }
    ]

    private phoneRules = [
      v => !!v || 'Phone number is required',
      v => !v || (v.length === 14) || 'Phone number is invalid'
    ]

    private extensionRules = [
      v => !v || (v.length >= 0 || v.length <= 4) || 'Extension is invalid'
    ]

    private firstNameRules = [
      v => !!v || 'First Name is Required'
    ]

    private lastNameRules = [
      v => !!v || 'Last Name is Required'
    ]

    private get isInEditNameMode () {
      // isExtraProvStepperOr
      return this.isAffidavitUpload || this.token || (this.isStepperView && (this.stepperSource === AccessType.EXTRA_PROVINCIAL))
    }

    private get isBCEIDUser (): boolean {
      return this.currentUser?.loginSource === LoginSource.BCEID
    }

    private emailMustMatch (): string {
      return (this.emailAddress === this.confirmedEmailAddress) ? '' : 'Email addresses must match'
    }

    private isFormValid (): boolean {
      return this.$refs.form &&
        this.$refs.form.validate() &&
        this.confirmedEmailAddress === this.emailAddress
    }

    private async mounted () {
      if (!this.userProfile) {
        await this.getUserProfile('@me')
      }
      let user: any = {}
      // clear user profile data
      if (!this.clearForm) {
        if (this.userProfileData) {
          user = this.userProfileData
        } else {
          user = { ...this.userProfile }
          user.email = this.userContact?.email
          user.phone = this.userContact?.phone
          user.phoneExtension = this.userContact?.phoneExtension
        }
      } else {
        user = this.userProfileData
      }
      this.firstName = user?.firstname || ''
      this.lastName = user?.lastname || ''
      this.emailAddress = user?.email || ''
      this.emailAddress = this.confirmedEmailAddress = user?.email || ''
      this.phoneNumber = user?.phone || ''
      this.extension = user?.phoneExtension || ''

      if (this.userContact) {
        this.editing = true
      }

      if (configHelper.getAuthResetAPIUrl()) {
        this.isTester = this.currentUser?.roles?.includes(Role.Tester)
      }
    }

    private async save () {
      if (this.isFormValid()) {
        const user:User = {
          firstname: this.firstName.trim(),
          lastname: this.lastName.trim()
        }
        const contact = {
          email: this.emailAddress.toLowerCase(),
          phone: this.phoneNumber,
          phoneExtension: this.extension
        }
        if (this.isBCEIDUser) {
          await this.updateUserFirstAndLastName(user)
        }
        await this.saveOrUpdateContact(contact)
        await this.getUserProfile('@me')
        // If a token was provided, that means we are in the accept invitation flow for users and account coordinators
        // Incase if it is accept invitation flow for account admin emit event for parent to let know user profile process is done
        if (this.isAffidavitUpload) {
          this.$emit('emit-admin-profile-complete')
          return
        }
        // so redirect to /confirmtoken
        if (this.token) {
          this.$router.push('/confirmtoken/' + this.token)
          return
        }
        this.redirectToNext()
      }
    }

    private next () {
      const userProfile = {
        firstname: this.firstName.trim(),
        lastname: this.lastName.trim(),
        email: this.emailAddress.toLowerCase(),
        phone: this.phoneNumber,
        phoneExtension: this.extension
      }
      this.setUserProfileData(userProfile)

      this.stepForward()
    }

    @Emit('final-step-action')
    private createAccount () {
    }

    private async saveOrUpdateContact (contact:Contact) {
      if (this.editing) {
        await this.updateUserContact(contact)
      } else {
        await this.createUserContact(contact)
      }
    }

    private redirectToNext () {
      if (CommonUtils.isUrl(this.getNextPageUrl())) {
        window.location.assign(appendAccountId(this.getNextPageUrl()))
      } else {
        this.$router.push(this.getNextPageUrl())
      }
    }

    private cancel () {
      if (this.isStepperView) {
        this.$router.push('/')
      } else {
        this.navigateBack()
      }
    }

    private navigateBack (): void {
      if (this.currentOrganization) {
        window.location.assign(configHelper.getBcrosDashboardURL())
      } else {
        this.$router.push('/home')
      }
    }

    private goBack () {
      if (this.isAffidavitUpload) {
        // emit event to let parent know about the previous step request
        this.$emit('emit-admin-profile-previous-step')
      } else {
        this.stepBack(this.currentOrganization!.orgType === this.ACCOUNT_TYPE.PREMIUM)
      }
    }

    private async deactivate (): Promise<void> {
      try {
        this.isDeactivating = true
        await UserService.deactivateUser()
        const redirectUri = encodeURIComponent(`${configHelper.getSelfURL()}/profiledeactivated`)
        this.$router.push(`/${Pages.SIGNOUT}/${redirectUri}`)
      } catch (exception) {
        this.$refs.deactivateUserFailureDialog.open()
      } finally {
        this.isDeactivating = false
      }
    }

    private cancelConfirmDeactivate () {
      this.$refs.deactivateUserConfirmationDialog.close()
    }

    private async reset (): Promise<void> {
      try {
        this.isReseting = true
        await UserService.resetUser()
        const redirectUri = encodeURIComponent(`${configHelper.getSelfURL()}/profiledeactivated`)
        this.$router.push(`/${Pages.SIGNOUT}/${redirectUri}`)
      } catch (exception) {
        this.$refs.resetFailureDialog.open()
      } finally {
        this.isReseting = false
      }
    }

    private cancelConfirmReset () {
      this.$refs.resetDialog.close()
    }
}
</script>

<style lang="scss" scoped>
.legal-name {
  font-size: 1.25rem !important;
  font-weight: 700;
  letter-spacing: -0.02rem;
}
.profile-subtitle {
  color: $gray7;
}
</style>
