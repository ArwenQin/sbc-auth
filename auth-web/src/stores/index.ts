import { PiniaVuePlugin, createPinia } from 'pinia'
import Vue from 'vue'
import { useActivityStore } from './activityLog'
import { useAppStore } from './app'
import { useBusinessStore } from './business'
import { useCodesStore } from './codes'
import { useOrgStore } from './org'
import { useStaffStore } from './staff'
import { useTaskStore } from './task'
import { useUserStore } from './user'

/**
 * Configures and returns Pinia Store.
 */
export function getPiniaStore () {
  Vue.use(PiniaVuePlugin)

  return createPinia()
}

export * from './app'
export * from './activityLog'
export * from './business'
export * from './codes'
export * from './org'
export * from './staff'
export * from './task'
export * from './user'
export * from 'sbc-common-components/src/stores'

/* Resets all values for a store, eg on Logout */
export function resetAllStores () {
  [
    useActivityStore(),
    useBusinessStore(),
    useCodesStore(),
    useOrgStore(),
    useStaffStore(),
    useTaskStore(),
    useUserStore(),
    useAppStore()
  ].forEach((store) => {
    store.$reset()
  })
}
