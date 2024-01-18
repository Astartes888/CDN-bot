import datetime
import json
import logging
from datetime import date, timedelta
from datetime import datetime
import aiohttp
from api.iiko_api_methods.exception import CheckTimeToken, SetSession, TokenException, PostException, ParamSetException
from api.iiko_api_methods.models import *


class BaseAPI:

    DEFAULT_TIMEOUT = "15"

    def __init__(self, api_login: str, session: Optional[aiohttp.ClientSession] = None, debug: bool = False,
                 base_url: str = None, working_token: str = None, base_headers: dict = None, logger: Optional[
            logging.Logger] = None, return_dict: bool = False):
        """

        :param api_login: login api iiko cloud
        :param session: session object
        :param debug: logging dict response
        :param base_url: url iiko cloud api
        :param working_token: Initialize an object based on a working token, that is, without requesting a new one
        :param base_headers: base header for request in iiko cloud api
        :param logger: your object Logger
        :param return_dict: return a dictionary instead of models
        """

        self.__session = session
        self.__api_login = api_login
        self.__token: Optional[str] = None
        self.__debug = debug
        self.__time_token: Optional[date] = None
        self.__organizations_ids_model: Optional[BaseOrganizationsModel] = None
        self.__organizations_ids: Optional[List[str]] = None
        self.__strfdt = "%Y-%m-%d %H:%M:%S.000"
        self.__return_dict = return_dict
        self.logger = logger if logger is not None else logging.getLogger()

        self.__base_url = "https://api-ru.iiko.services" if base_url is None else base_url
        self.__headers = {
            "Content-Type": "application/json",
            "Timeout": "45",
        } if base_headers is None else base_headers

        self.__last_data = None

    async def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession()
    
    async def get_session(self) -> Optional[aiohttp.ClientSession]:
        if self.__session is None or self.__session.closed:
            self.__session = await self.get_new_session()

        if not self.__session._loop.is_running():
            await self.__session.close()
            self.__session = await self.get_new_session()
        return self.__session

    @classmethod
    async def init_class(cls, api_login: str, session: Optional[aiohttp.ClientSession] = None, debug: bool = False, 
                         base_url: str = None, working_token: str = None, base_headers: dict = None, logger: Optional[
                             logging.Logger] = None, return_dict: bool = False):
        
        self = cls(api_login=api_login, session=session, debug=debug, base_url=base_url, working_token=working_token,
                   base_headers=base_headers, logger=logger, return_dict=return_dict)
           
        if working_token is not None:
            await self.__set_token(working_token)
        else:
            await self.__get_access_token()
        
        return self

    async def check_status_code_token(self, code: Union[str, int]):
        if str(code) == "401":
            await self.__get_access_token()
        elif str(code) == "400":
            pass
        elif str(code) == "408":
            pass
        elif str(code) == "500":
            pass

    async def check_token_time(self) -> bool:
        """
        Проверка на время жизни маркера доступа
        :return: Если прошло 15 мин будет запрошен токен и метод вернёт True, иначе вернётся False
        """
        fifteen_minutes_ago = datetime.now() - timedelta(minutes=15)
        time_token = self.__time_token
        try:

            if time_token <= fifteen_minutes_ago:
                await self.__get_access_token()
                return True
            else:
                return False
        except TypeError:
            raise CheckTimeToken(
                self.__class__.__qualname__,
                self.check_token_time.__name__,
                f"Не запрошен Token и не присвоен объект типа datetime.datetime")

    @property
    async def organizations_ids_models(self) -> Optional[List[OrganizationModel]]:
        return await self.__organizations_ids_model

    @property
    async def organizations_ids(self) -> Optional[List[str]]:
        return await self.__organizations_ids

    @property
    async def last_data(self) -> Optional[List[str]]:
        return await self.__last_data

    @property
    async def session_s(self) -> aiohttp.ClientSession:
        """Вывести сессию"""
        return await self.get_session() #self.__session

    @session_s.setter
    async def session_s(self, session: aiohttp.ClientSession = None):
        """Изменение сессии"""
        if session is None:
            raise SetSession(
                self.__class__.__qualname__,
                self.session_s.__name__,
                f"Не присвоен объект типа aiohttp.ClientSession")
        else:
            self.__session = session

    @property
    async def time_token(self):
        return await self.__time_token

    @property
    async def api_login(self) -> str:
        return await self.__api_login

    @property
    async def token(self) -> str:
        return await self.__token

    @property
    async def base_url(self):
        return await self.__base_url

    @base_url.setter
    async def base_url(self, value: str):
        self.__base_url = await value

    @property
    async def strfdt(self):
        return await self.__strfdt

    @strfdt.setter
    async def strfdt(self, value: str):
        self.__strfdt = await value

    @property
    async def headers(self):
        return await self.__headers

    @headers.setter
    async def headers(self, value: str):
        self.__headers = await value

    @property
    async def return_dict(self):
        return await self.__return_dict

    @return_dict.setter
    async def return_dict(self, value: str):
        self.__return_dict = await value

    @property
    async def timeout(self):
        return await self.__headers.get("Timeout")


    def set_timeout(self, value: int):
        self.__headers.update({"Timeout": str(value)})


    def del_timeout(self):
        self.__headers.update({"Timeout": str(self.DEFAULT_TIMEOUT)})

    async def __set_token(self, token):
        self.__token = token
        self.__headers["Authorization"] = f"Bearer {token}"
        self.__time_token = datetime.now()

    async def access_token(self):
        """Получить маркер доступа"""
        data = json.dumps({"apiLogin": self.__api_login})
        conn = await self.session_s
        try:
            async with conn.post(f'{self.__base_url}/api/1/access_token', json=data) as result:
                response_data = await result.read()
                response_data: dict = json.loads(response_data)

                if response_data.get("errorDescription", None) is not None:
                    raise TypeError(f'{response_data=}')

                if response_data.get("token", None) is not None:
                    await self.check_status_code_token(result.status)
                    await self.__set_token(response_data.get("token", ""))

        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                self.access_token.__name__,
                                f"Не удалось получить маркер доступа: \n{err}")
        except TypeError as err:
            raise TokenException(self.__class__.__qualname__,
                                self.access_token.__name__,
                                f"Не удалось получить маркер доступа: \n{err}")

    async def _post_request(self, url: str, data: dict = None, timeout=DEFAULT_TIMEOUT, model_response_data=None,
                      model_error=CustomErrorModel):
        if data is None:
            data = {}
        if timeout != self.DEFAULT_TIMEOUT:
            self.set_timeout(timeout)
        self.logger.info(f"{url=}, {data=}, {model_response_data=}, {model_error=}")
        conn = await self.session_s
        async with conn.post(f'{self.__base_url}{url}', json=data, headers=self.__headers) as response:
            if response.status == 401:
                await self.__get_access_token()
                return await self._post_request(url=url, data=data, timeout=timeout, model_response_data=model_response_data,
                                        model_error=model_error)

            if self.__debug:
                try:
                    await self.logger.debug(
                        f"Входные данные:\n{url=}\n{json.dumps(data)=}\n{self.__headers=}\n\nВыходные данные:\n{response.headers=}\n{response.read()=}\n\n")
                except Exception as err:
                    self.logger.debug(f"{err=}")
            response_data = await response.read()
            response_data: dict = json.loads(response_data)
            self.__last_data = response_data
            if self.__return_dict:
                return response_data
            if response_data.get("errorDescription", None) is not None:
                error_model = model_error.model_validate(response_data)
                error_model.status_code = response.status
                return error_model
            if model_response_data is not None:
                return model_response_data.model_validate(response_data)
            self.del_timeout()
            return response_data

    async def __get_access_token(self):
        out = await self.access_token()
        if isinstance(out, CustomErrorModel):
            raise TokenException(self.__class__.__qualname__,
                                 self.access_token.__name__,
                                 f"Не удалось получить маркер доступа: \n{out}")

    async def __convert_org_data(self, data: BaseOrganizationsModel):
        self.__organizations_ids = data.__list_id__()

    async def organizations(self, organization_ids: List[str] = None, return_additional_info: bool = None,
                      include_disabled: bool = None, return_external_data: bool = None, timeout=DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseOrganizationsModel]:
        """
        Возвращает организации, доступные пользователю по API-login.
        :param organization_ids: ID организаций, информацию по которым нужно получить. По умолчанию все организации из apiLogin.
        :param return_additional_info: Указываем, если нужно получить дополнительную информацию об организациях (RMS версия, страна, адрес заведения, и т.д.), 
        или будет возвращена минимальное инфо (id и название организации).
        :param include_disabled: Показывает, что ответ содержит отключенные организации.
        :return: Возвращает информацию об организации(организациях) в виде модели данных BaseOrganizationsModel или пользовательское исключение CustomErrorModel
        """
        
        data = {}
        if organization_ids is not None:
            data["organizationIds"] = organization_ids
        if return_additional_info is not None:
            data["returnAdditionalInfo"] = return_additional_info
        if include_disabled is not None:
            data["includeDisabled"] = include_disabled
        if return_external_data is not None:
            data["returnExternalData"] = return_external_data
        try:

            response_data = await self._post_request(
                url="/api/1/organizations",
                data=data,
                model_response_data=BaseOrganizationsModel,
                timeout=timeout
            )
            if isinstance(response_data, BaseOrganizationsModel):
                await self.__convert_org_data(data=response_data)
            return response_data


        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.organizations.__name__,
                                 f"Не удалось получить организации: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.organizations.__name__,
                            f"Не удалось получить организации: \n{err}")


class Dictionaries(BaseAPI):
    async def cancel_causes(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseCancelCausesModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.cancel_causes.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return await self._post_request(
                url="/api/1/cancel_causes",
                data=data,
                model_response_data=BaseCancelCausesModel,
                timeout=timeout
            )
        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.cancel_causes.__name__,
                                 f"Не удалось получить причины отмены доставки: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.cancel_causes.__name__,
                            f"Не удалось получить причины отмены доставки: \n{err}")

    async def order_types(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseOrderTypesModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.order_types.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return await self._post_request(
                url="/api/1/deliveries/order_types",
                data=data,
                model_response_data=BaseOrderTypesModel,
                timeout=timeout
            )
        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.order_types.__name__,
                                 f"Не удалось получить типы заказа: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.order_types.__name__,
                            f"Не удалось получить типы заказа: \n{err}")

    async def discounts(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseDiscountsModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.discounts.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return await self._post_request(
                url="/api/1/discounts",
                data=data,
                model_response_data=BaseDiscountsModel,
                timeout=timeout
            )
        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.discounts.__name__,
                                 f"Не удалось получить скидки/надбавки: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.discounts.__name__,
                            f"Не удалось получить скидки/надбавки: \n{err}")

    async def payment_types(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BasePaymentTypesModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.payment_types.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return await self._post_request(
                url="/api/1/payment_types",
                data=data,
                model_response_data=BasePaymentTypesModel,
                timeout=timeout
            )
        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.payment_types.__name__,
                                 f"Не удалось получить типы оплаты: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.payment_types.__name__,
                            f"Не удалось получить типы оплаты: \n{err}")

    async def removal_types(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, BaseRemovalTypesModel]:
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.removal_types.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        try:

            return await self._post_request(
                url="/api/1/removal_types",
                data=data,
                model_response_data=BaseRemovalTypesModel,
                timeout=timeout
            )
        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.removal_types.__name__,
                                 f"Не удалось получить removal_types: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.removal_types.__name__,
                            f"Не удалось получить removal_types: \n{err}")

    async def tips_types(self, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[CustomErrorModel, BaseTipsTypesModel]:
        try:

            return await self._post_request(
                url="/api/1/tips_types",
                model_response_data=BaseTipsTypesModel,
                timeout=timeout
            )
        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.removal_types.__name__,
                                 f"Не удалось получить подсказки для группы api-logins rms: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.removal_types.__name__,
                            f"Не удалось получить подсказки для группы api-logins rms: \n{err}")


class DiscountPromotion(BaseAPI):
    async def coupons_series(self, organization_id: str) -> Union[
        CustomErrorModel, SeriesWithNotActivatedCoupon]:
        if not bool(organization_id):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.coupons_series.__name__,
                                    f"Отсутствует аргумент id организации")
        data = {
            "organizationId": organization_id,
        }
        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/coupons/series",
                data=data,
                model_response_data=SeriesWithNotActivatedCoupon,
            )
        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.coupons_series.__name__,
                                 f"Не удалось получить промокоды: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.coupons_series.__name__,
                            f"Не удалось получить промокоды: \n{err}")

    async def coupons_info(self, organization_id: str, number: str, series: str = None) -> Union[
        CustomErrorModel, BaseCouponInfo]:
        if not bool(organization_id):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.coupons_info.__name__,
                                    f"Отсутствует аргумент id организации")
        data = {
            "number": number,
            "series": series,
            "organizationId": organization_id,
        }
        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/coupons/info",
                data=data,
                model_response_data=BaseCouponInfo,
            )
        except aiohttp.ClientError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.coupons_info.__name__,
                                 f"Не удалось получить промокоды: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.coupons_info.__name__,
                            f"Не удалось получить промокоды: \n{err}")


class Customers(BaseAPI):
    async def customer_info(self, organization_id: str, type: TypeRCI, identifier: str, timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[
        CustomErrorModel, CustomerInfoModel]:
        """
        Обязательные параметры:
        :param organization_id: Id организации соответственно
        :param identifier: Идентификатор по типу (критерию) поиска
        :param type: Тип (критерий) поиска phone или cardTrack, или cardNumber, или email, или id клиента
        :return: Возвращает информацию о клиенте в виде модели данных CustomerInfoModel или пользовательское исключение CustomErrorModel
        """
        if not bool(organization_id):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.customer_info.__name__,
                                    f"Отсутствует аргумент id организации")
        
        if not bool(identifier):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.customer_info.__name__,
                                    f"Отсутствует аргумент идентификатор по типу поиска")
        
        if not bool(type):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.customer_info.__name__,
                                    f"Отсутствует аргумент типа поиска")
        
        data = {
            "organizationId": organization_id,
            "type": type,
        }
        if type == TypeRCI.phone.value:
            data[TypeRCI.phone.value] = identifier
        elif type == TypeRCI.card_track.value:
            data[TypeRCI.card_track.value] = identifier
        elif type == TypeRCI.card_number.value:
            data[TypeRCI.card_number.value] = identifier
        elif type == TypeRCI.email.value:
            data[TypeRCI.email.value] = identifier
        elif type == TypeRCI.id.value:
            data[TypeRCI.id.value] = identifier

        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/info",
                data=data,
                model_response_data=CustomerInfoModel,
                timeout=timeout
            )

        except aiohttp.ClientError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_info.__name__,
                                f"Не удалось получить информацию о клиенте: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_info.__name__,
                                f"Не удалось: \n{err}")

    async def customer_create_or_update(
        self,
        organization_id: str,
        phone: Optional[str] = None,
        card_track: Optional[str] = None,
        card_number: Optional[str] = None,
        name: Optional[str] = None,
        middle_name: Optional[str] = None,
        sur_name: Optional[str] = None,
        birthday: Optional[str] = None,
        email: Optional[str] = None,
        sex: Optional[str] = None,
        consent_status: Optional[str] = None,
        should_receive_promo_actions_info: Optional[bool] = None,
        referrer_id: Optional[str] = None,
        user_data: Optional[str] = None,
        id: str = None,
        timeout=BaseAPI.DEFAULT_TIMEOUT)-> Union[
        CustomErrorModel, CustomerCreateOrUpdateModel]:

        """
        Обязательные параметры:
        :param organization_id: Id организации соответственно
        Остальные параметры клиента указываются по необходимости внесения или обновления и являются опциональными
        :return: Возвращает id клиента или пользовательское исключение CustomErrorModel
        """

        data = {
            "organizationId": organization_id,
        }
        if id is not None:
            data['id'] = id
        if phone is not None:
            data['phone'] = phone
        if card_track is not None:
            data['cardTrack'] = card_track
        if card_number is not None:
            data['cardNumber'] = card_number
        if name is not None:
            data['name'] = name
        if middle_name is not None:
            data['middleName'] = middle_name
        if sur_name is not None:
            data['surName'] = sur_name
        if birthday is not None:
            data['birthday'] = birthday
        if email is not None:
            data['email'] = email
        if sex is not None:
            data['sex'] = sex
        if consent_status is not None:
            data['consentStatus'] = consent_status
        if should_receive_promo_actions_info is not None:
            data['shouldReceivePromoActionsInfo'] = should_receive_promo_actions_info
        if referrer_id is not None:
            data['referrerId'] = referrer_id
        if user_data is not None:
            data['userData'] = user_data

        try:
            return await self._post_request(
                url="/api/1/loyalty/iiko/customer/create_or_update",
                data=data,
                model_response_data=CustomerCreateOrUpdateModel,
                timeout=timeout
            )

        except aiohttp.ClientError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_create_or_update.__name__,
                                f"Не удалось создать или обновить клиента: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.customer_create_or_update.__name__,
                                f"Не удалось: \n{err}")


    async def refill_balance(self, organization_id: str, 
                            customer_id: Optional[str] = None, 
                            wallet_id: Optional[str]= None, 
                            sum: Union[str, int, None] = None,
                            comment: Optional[str] = None, 
                            timeout=BaseAPI.DEFAULT_TIMEOUT) -> Optional[CustomErrorModel]:
            """
            Обязательные параметры:
            :param organization_id: Id организации соответственно
            :param customer_id: Id клиента
            :param wallet_id: Id кошелька клиента
            Остальные параметры указываются по необходимости для пополнения баланса и являются опциональными
            :return: None или пользовательское исключение CustomErrorModel
            """
            if not bool(organization_id):
                raise ParamSetException(self.__class__.__qualname__,
                                        self.refill_balance.__name__,
                                        f"Отсутствует аргумент id организации")
            
            data = {
                "organizationId": organization_id,
            }

            if customer_id is not None:
                data['customerId'] = customer_id
            if wallet_id is not None:
                data['walletId'] = wallet_id
            if sum is not None:
                data['sum'] = sum
            if comment is not None:
                data['comment'] = comment          

            try:
                return await self._post_request(
                    url="/api/1/loyalty/iiko/customer/wallet/topup",
                    data=data,
                    timeout=timeout
                )

            except aiohttp.ClientError as err:
                raise PostException(self.__class__.__qualname__,
                                    self.customer_info.__name__,
                                    f"Не удалось выполнить запрос: \n{err}")
            except TypeError as err:
                raise PostException(self.__class__.__qualname__,
                                    self.customer_info.__name__,
                                    f"Не удалось: \n{err}")

    async def withdraw_balance(self, organization_id: str, 
                                customer_id: Optional[str], 
                                wallet_id: Optional[str], 
                                sum: Union[str, int, None] = None,
                                comment: Optional[str] = None, 
                                timeout=BaseAPI.DEFAULT_TIMEOUT) -> Optional[CustomErrorModel]:
                """
                Обязательные параметры:
                :param organization_id: Id организации соответственно
                :param customer_id: Id клиента
                :param wallet_id: Id кошелька клиента
                Остальные параметры указываются по необходимости для списания с баланса и являются опциональными
                :return: None или пользовательское исключение CustomErrorModel
                """
                if not bool(organization_id):
                    raise ParamSetException(self.__class__.__qualname__,
                                            self.refill_balance.__name__,
                                            f"Отсутствует аргумент id организации")
                
                data = {
                    "organizationId": organization_id,
                }

                if customer_id is not None:
                    data['customerId'] = customer_id
                if wallet_id is not None:
                    data['walletId'] = wallet_id
                if sum is not None:
                    data['sum'] = str(sum)
                if comment is not None:
                    data['comment'] = comment          

                try:
                    return await self._post_request(
                        url="/api/1/loyalty/iiko/customer/wallet/chargeoff",
                        data=data,
                        timeout=timeout
                    )

                except aiohttp.ClientError as err:
                    raise PostException(self.__class__.__qualname__,
                                        self.customer_info.__name__,
                                        f"Не удалось выполнить запрос: \n{err}")
                except TypeError as err:
                    raise PostException(self.__class__.__qualname__,
                                        self.customer_info.__name__,
                                        f"Не удалось: \n{err}")
            

class IikoTransport (Dictionaries, Customers, DiscountPromotion):
    pass

#Orders, Deliveries, Employees, Address, DeliveryRestrictions, TerminalGroup, Menu, Dictionaries, DiscountPromotion, Commands, Notifications, Customers