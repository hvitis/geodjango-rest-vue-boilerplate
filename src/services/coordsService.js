import api from '@/services/api'

export default {
  getCoordsFromAddress(queryAddress) {
    return api.get(`accounts/coordinates?address=${queryAddress}`)
              .then(response => response.data.coordinates)
  },
}