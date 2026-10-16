"""DomainApi: API methods of the Domain section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from .models import DomainDeleteRequest, DomainDeleteResponse, DomainGetDnsRecordsRequest, DomainGetDnsRecordsResponse, DomainGetSandboxDomainResponse, DomainListRequest, DomainListResponse, DomainValidateDkimRequest, DomainValidateDkimResponse, DomainValidateVerificationRecordRequest, DomainValidateVerificationRecordResponse


class DomainApi:
    """You can use these methods to setup sender domains and check their statuses. They might be useful in
    case you want to automate adding domains for your own clients.

    To add new sender domain thru API you should take following steps:
    - Get DNS records with [domain/get-dns-records](https://docs.unione.io/en/web-api-ref#domain-get-dns-records) method and add them to your DNS provider.
    - Every 5-10 minutes call [domain/list](https://docs.unione.io/en/web-api-ref#domain-list) method for your domain (or several domains) and check verification-record.status and dkim.status in the response. You can call it more often if you like, but please not more than once per minute.
    - If verification-record.status="unconfirmed" then you should call [domain/validate-verification-record](https://docs.unione.io/en/web-api-ref#domain-validate-verification-record) to trigger verification record validation.
    - If dkim.status="inactive" then start DKIM checking by calling [domain/validate-dkim](https://docs.unione.io/en/web-api-ref#domain-validate-dkim) (UniOne itself checks  DKIM every 30 minutes also)
    - When you get verification-record.status="confirmed" and dkim.status="active" for the domain then you can stop checking it's status with domain/list and start using it as a sender domain.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def get_dns_records(self, request: DomainGetDnsRecordsRequest) -> DomainGetDnsRecordsResponse:
        """Returns info on domain DNS setup for using with UniOne.

        In order to send emails you have to confirm that you own the domain that you are going to send
        emails from and setup DKIM signature for the domain. This method allows you to register your domain
        in UniOne and generate verification record and DKIM key, or return previously generated ones if
        domain is already registered.
        You should add then DNS records like this to all of the domains you want to confirm:

        `@             IN TXT "unione-validate-hash=483bb362ebdbeedd755cfb1d4d661"`

        `us._domainkey IN TXT "k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDo7"`

        `@             IN TXT  "v=spf1 include:spf.unione.io ~all"`

        - First record value should contain "verification-record" field returned by get-dns-records method "as is".
        - Second record value should contain "dkim" field value after "p=". Mind the name of this record! "us._domainkey." prefix is important for DKIM selector of UniOne to work properly.
        - Third record contains optional, but very recommended SPF entry. Probably you already have one, then just add append include:spf.unione.io right after v=spf1.

        Syntax requirements of different DNS providers may differ:
        - sometimes it's necesarry to put full domain name instead of @ sign.
        - some providers require add TTL value (like 3600)
        - some providers don't require quotes for enclosing values
        Please check requirements of your provider and advice your users to do it.

        Documentation: https://docs.unione.io/en/web-api-ref#domain-get-dns-records

        Raises ApiError when the API returns an error.
        """
        return DomainGetDnsRecordsResponse.from_dict(self._client.call("/domain/get-dns-records.json", request.to_dict()))

    def validate_verification_record(self, request: DomainValidateVerificationRecordRequest) -> DomainValidateVerificationRecordResponse:
        """Triggers verification record validation for domain.

        If you get 200 OK then it means the validation process started succesfully, but it doesn't mean the
        verification record is valid. You should check later verification-record.status field returned by
        [domain/list](https://docs.unione.io/en/web-api-ref#domain-list) method to get the result. Please
        read more [here](https://docs.unione.io/en/web-api-ref#domain).

        Documentation: https://docs.unione.io/en/web-api-ref#domain-validate-verification-record

        Raises ApiError when the API returns an error.
        """
        return DomainValidateVerificationRecordResponse.from_dict(self._client.call("/domain/validate-verification-record.json", request.to_dict()))

    def validate_dkim(self, request: DomainValidateDkimRequest) -> DomainValidateDkimResponse:
        """Validates DKIM record for domain.

        If you get 200 OK then it means the validation process started succesfully, but it doesn't mean the
        DKIM record is valid. You should check later dkim.status field returned by
        [domain/list](https://docs.unione.io/en/web-api-ref#domain-list) method to get the result. Please
        read more [here](https://docs.unione.io/en/web-api-ref#domain).

        Documentation: https://docs.unione.io/en/web-api-ref#domain-validate-dkim

        Raises ApiError when the API returns an error.
        """
        return DomainValidateDkimResponse.from_dict(self._client.call("/domain/validate-dkim.json", request.to_dict()))

    def list(self, request: DomainListRequest) -> DomainListResponse:
        """Returns a list of all registered domains for user or project, together with statuses of last
        validations.

        Returns last status of ownership validation and DKIM validation for each domain. Read more
        [here](https://docs.unione.io/en/web-api-ref#domain).

        Documentation: https://docs.unione.io/en/web-api-ref#domain-list

        Raises ApiError when the API returns an error.
        """
        return DomainListResponse.from_dict(self._client.call("/domain/list.json", request.to_dict()))

    def get_sandbox_domain(self) -> DomainGetSandboxDomainResponse:
        """Creates a sandbox domain for the account or returns the existing one.

        Returns an account sandbox domain that is ready for use in the `from_email` field of
        [email/send](https://docs.unione.io/en/web-api-ref#email-send). If the account has no sandbox
        domain, UniOne creates one and returns it. Repeated calls return the same domain.

        The method is available only with an account API key. Project API keys cannot create sandbox
        domains.

        Documentation: https://docs.unione.io/en/web-api-ref#domain-get-sandbox-domain

        Raises ApiError when the API returns an error.
        """
        return DomainGetSandboxDomainResponse.from_dict(self._client.call("/domain/get-sandbox-domain.json"))

    def delete(self, request: DomainDeleteRequest) -> DomainDeleteResponse:
        """Deletes a domain. Attention: you should use project's API key to delete a project's domain.

        Deletes a domain.

        Documentation: https://docs.unione.io/en/web-api-ref#domain-delete

        Raises ApiError when the API returns an error.
        """
        return DomainDeleteResponse.from_dict(self._client.call("/domain/delete.json", request.to_dict()))
