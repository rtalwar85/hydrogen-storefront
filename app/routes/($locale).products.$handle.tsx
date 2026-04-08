import {redirect, useLoaderData} from 'react-router';
import type {Route} from './+types/products.$handle';
import {
  getSelectedProductOptions,
  Analytics,
  useOptimisticVariant,
  getProductOptions,
  getAdjacentAndFirstAvailableVariants,
  useSelectedOptionInUrlParam,
} from '@shopify/hydrogen';
import {ProductPrice} from '~/components/ProductPrice';
import {ProductImage} from '~/components/ProductImage';
import {ProductForm} from '~/components/ProductForm';
import {redirectIfHandleIsLocalized} from '~/lib/redirect';

export const meta: Route.MetaFunction = ({data}) => {
  return [
    {title: `Hydrogen | ${data?.product.title ?? ''}`},
    {
      rel: 'canonical',
      href: `/products/${data?.product.handle}`,
    },
  ];
};

export async function loader(args: Route.LoaderArgs) {
  const deferredData = loadDeferredData(args);
  const criticalData = await loadCriticalData(args);

  return {...deferredData, ...criticalData};
}

async function loadCriticalData({context, params, request}: Route.LoaderArgs) {
  const {handle} = params;
  const {storefront} = context;

  if (!handle) {
    throw new Error('Expected product handle to be defined');
  }

  const [{product}] = await Promise.all([
    storefront.query(PRODUCT_QUERY, {
      variables: {handle, selectedOptions: getSelectedProductOptions(request)},
    }),
  ]);

  if (!product?.id) {
    throw new Response(null, {status: 404});
  }

  redirectIfHandleIsLocalized(request, {handle, data: product});

  return {
    product,
  };
}

function loadDeferredData({context, params}: Route.LoaderArgs) {
  return {};
}

export default function Product() {
  const {product} = useLoaderData<typeof loader>();

  const selectedVariant = useOptimisticVariant(
    product.selectedOrFirstAvailableVariant,
    getAdjacentAndFirstAvailableVariants(product),
  );

  useSelectedOptionInUrlParam(selectedVariant.selectedOptions);

  const productOptions = getProductOptions({
    ...product,
    selectedOrFirstAvailableVariant: selectedVariant,
  });

  const {title, descriptionHtml, vendor, handle} = product;
  const imageGallery = product.images?.nodes ?? [];
  const selectedColor = selectedVariant?.selectedOptions.find((option) =>
    option.name.toLowerCase().includes('color'),
  )?.value;
  const selectedSize = selectedVariant?.selectedOptions.find((option) =>
    option.name.toLowerCase().includes('size'),
  )?.value;

  return (
    <section className="product-page">
      <div className="product">
        <div className="product-media-column">
          <div className="product-breadcrumbs" aria-label="Breadcrumb">
            <span>Home</span>
            <span>/</span>
            <span>Shop</span>
            <span>/</span>
            <span>{vendor}</span>
          </div>
          <ProductImage
            image={selectedVariant?.image}
            images={imageGallery}
            title={title}
          />
        </div>

        <div className="product-main">
          <div className="product-panel">
            <p className="product-eyebrow">{vendor}</p>
            <h1>{title}</h1>
            <div className="product-price-block">
              <ProductPrice
                price={selectedVariant?.price}
                compareAtPrice={selectedVariant?.compareAtPrice}
              />
              <p className="product-tax-note">
                Shipping options are calculated at checkout.
              </p>
            </div>

            <div className="product-highlights" aria-label="Product highlights">
              <span>New season energy</span>
              <span>Easy day-to-night styling</span>
              <span>Fast add-to-bag experience</span>
            </div>

            {(selectedColor || selectedSize) && (
              <div className="product-selected-summary">
                {selectedColor ? <span>Colour: {selectedColor}</span> : null}
                {selectedSize ? <span>Size: {selectedSize}</span> : null}
              </div>
            )}

            <ProductForm
              productOptions={productOptions}
              selectedVariant={selectedVariant}
            />

            <div className="product-utility-row">
              <span>SKU: {selectedVariant?.sku || handle}</span>
              <span>
                {selectedVariant?.availableForSale
                  ? 'In stock'
                  : 'Currently unavailable'}
              </span>
            </div>
          </div>

          <div className="product-details-stack">
            <details className="product-detail" open>
              <summary>Description</summary>
              <div dangerouslySetInnerHTML={{__html: descriptionHtml}} />
            </details>
            <details className="product-detail">
              <summary>Fit & styling</summary>
              <div>
                <p>
                  Style this piece with statement accessories and denim, or
                  keep it minimal for a cleaner everyday look.
                </p>
              </div>
            </details>
            <details className="product-detail">
              <summary>Shipping & returns</summary>
              <div>
                <p>
                  Shipping methods and delivery estimates appear at checkout
                  before payment is completed.
                </p>
              </div>
            </details>
          </div>
        </div>
      </div>
      <Analytics.ProductView
        data={{
          products: [
            {
              id: product.id,
              title: product.title,
              price: selectedVariant?.price.amount || '0',
              vendor: product.vendor,
              variantId: selectedVariant?.id || '',
              variantTitle: selectedVariant?.title || '',
              quantity: 1,
            },
          ],
        }}
      />
    </section>
  );
}

const PRODUCT_VARIANT_FRAGMENT = `#graphql
  fragment ProductVariant on ProductVariant {
    availableForSale
    compareAtPrice {
      amount
      currencyCode
    }
    id
    image {
      __typename
      id
      url
      altText
      width
      height
    }
    price {
      amount
      currencyCode
    }
    product {
      title
      handle
    }
    selectedOptions {
      name
      value
    }
    sku
    title
    unitPrice {
      amount
      currencyCode
    }
  }
` as const;

const PRODUCT_FRAGMENT = `#graphql
  fragment Product on Product {
    id
    title
    vendor
    handle
    descriptionHtml
    description
    encodedVariantExistence
    encodedVariantAvailability
    options {
      name
      optionValues {
        name
        firstSelectableVariant {
          ...ProductVariant
        }
        swatch {
          color
          image {
            previewImage {
              url
            }
          }
        }
      }
    }
    selectedOrFirstAvailableVariant(selectedOptions: $selectedOptions, ignoreUnknownOptions: true, caseInsensitiveMatch: true) {
      ...ProductVariant
    }
    adjacentVariants (selectedOptions: $selectedOptions) {
      ...ProductVariant
    }
    images(first: 8) {
      nodes {
        id
        url
        altText
        width
        height
      }
    }
    seo {
      description
      title
    }
  }
  ${PRODUCT_VARIANT_FRAGMENT}
` as const;

const PRODUCT_QUERY = `#graphql
  query Product(
    $country: CountryCode
    $handle: String!
    $language: LanguageCode
    $selectedOptions: [SelectedOptionInput!]!
  ) @inContext(country: $country, language: $language) {
    product(handle: $handle) {
      ...Product
    }
  }
  ${PRODUCT_FRAGMENT}
` as const;
